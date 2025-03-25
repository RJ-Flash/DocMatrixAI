#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
REMOTE_USER="ixkhjgte"
REMOTE_HOST="docmatrixai.com"
API_PATH="/home1/ixkhjgte/api.docmatrixai.com"
WEBSITE_PATH="/home1/ixkhjgte/docmatrixai.com"
BACKUP_PATH="/home1/ixkhjgte/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${BLUE}Starting full deployment...${NC}"

# 1. Create backups
echo -e "${BLUE}Creating backups...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    mkdir -p $BACKUP_PATH/api $BACKUP_PATH/website
    
    # Backup API
    if [ -d $API_PATH ]; then
        cd $API_PATH
        tar -czf $BACKUP_PATH/api/backup_$TIMESTAMP.tar.gz .
    fi
    
    # Backup Website
    cd $WEBSITE_PATH
    tar -czf $BACKUP_PATH/website/backup_$TIMESTAMP.tar.gz .
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Backup failed! Aborting deployment.${NC}"
    exit 1
fi

# 2. Deploy API
echo -e "${BLUE}Deploying API...${NC}"
rsync -avz --delete \
    --exclude 'node_modules' \
    --exclude '.env' \
    --exclude 'logs' \
    --exclude '.git' \
    --exclude 'tmp' \
    ./api.docmatrixai.com/ $REMOTE_USER@$REMOTE_HOST:$API_PATH/

if [ $? -ne 0 ]; then
    echo -e "${RED}API deployment failed!${NC}"
    exit 1
fi

# 3. Deploy Website
echo -e "${BLUE}Deploying Website...${NC}"
rsync -avz --delete \
    --exclude 'node_modules' \
    --exclude '.env' \
    --exclude '.git' \
    --exclude 'tmp' \
    ./docmatrixai.com/ $REMOTE_USER@$REMOTE_HOST:$WEBSITE_PATH/

if [ $? -ne 0 ]; then
    echo -e "${RED}Website deployment failed!${NC}"
    exit 1
fi

# 4. Setup and Restart Services
echo -e "${BLUE}Setting up services...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    # Setup API
    cd $API_PATH
    npm ci --production
    NODE_ENV=production node scripts/migrate.js
    
    # Restart API with PM2
    if pm2 list | grep -q 'api-docmatrix'; then
        pm2 reload api-docmatrix
    else
        pm2 start ecosystem.config.js
    fi
    
    # Start monitoring
    if pm2 list | grep -q 'api-monitor'; then
        pm2 reload api-monitor
    else
        pm2 start monitoring/monitor.js --name api-monitor
    fi
    
    # Save PM2 configuration
    pm2 save
    
    # Set permissions
    chmod -R 755 $API_PATH
    find $API_PATH -type f -exec chmod 644 {} \;
    chmod 600 $API_PATH/.env
    
    chmod -R 755 $WEBSITE_PATH
    find $WEBSITE_PATH -type f -exec chmod 644 {} \;
    chmod 600 $WEBSITE_PATH/.env
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Service setup failed! Rolling back...${NC}"
    ssh $REMOTE_USER@$REMOTE_HOST "
        # Restore API
        cd $API_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/api/backup_$TIMESTAMP.tar.gz -C $API_PATH
        
        # Restore Website
        cd $WEBSITE_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/website/backup_$TIMESTAMP.tar.gz -C $WEBSITE_PATH
        
        # Restart services
        npm ci --production
        pm2 reload api-docmatrix
    "
    exit 1
fi

# 5. Verify deployment
echo -e "${BLUE}Verifying deployment...${NC}"
sleep 5 # Wait for services to start

# Check API health
API_HEALTH=$(curl -s https://api.docmatrixai.com/health)
if [[ $API_HEALTH != *"healthy"* ]]; then
    echo -e "${RED}API verification failed! Rolling back...${NC}"
    ssh $REMOTE_USER@$REMOTE_HOST "
        cd $API_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/api/backup_$TIMESTAMP.tar.gz -C $API_PATH
        npm ci --production
        pm2 reload api-docmatrix
    "
    exit 1
fi

# Check Website
WEBSITE_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" https://docmatrixai.com)
if [[ $WEBSITE_HEALTH != "200" ]]; then
    echo -e "${RED}Website verification failed! Rolling back...${NC}"
    ssh $REMOTE_USER@$REMOTE_HOST "
        cd $WEBSITE_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/website/backup_$TIMESTAMP.tar.gz -C $WEBSITE_PATH
    "
    exit 1
fi

# 6. Clean up old backups (keep last 7 days)
echo -e "${BLUE}Cleaning up old backups...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    find $BACKUP_PATH -type f -mtime +7 -name 'backup_*.tar.gz' -delete
"

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "You can verify the deployment at:"
echo -e "  - Website: https://docmatrixai.com"
echo -e "  - API: https://api.docmatrixai.com"
echo -e "  - API Health: https://api.docmatrixai.com/health"
echo -e "\nMonitoring:"
echo -e "  - Logs: tail -f /home1/ixkhjgte/logs/api-*.log"
echo -e "  - PM2: pm2 monit"
