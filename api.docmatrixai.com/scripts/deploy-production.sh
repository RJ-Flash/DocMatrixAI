#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
REMOTE_USER="ixkhjgte"
REMOTE_HOST="docmatrixai.com"
REMOTE_PATH="/home1/ixkhjgte/api.docmatrixai.com"
LOCAL_PATH="."
BACKUP_PATH="/home1/ixkhjgte/backups/api"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${BLUE}Starting deployment to production...${NC}"

# 1. Create backup
echo -e "${BLUE}Creating backup...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    mkdir -p $BACKUP_PATH
    cd $REMOTE_PATH
    tar -czf $BACKUP_PATH/backup_$TIMESTAMP.tar.gz .
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Backup failed! Aborting deployment.${NC}"
    exit 1
fi

# 2. Deploy files
echo -e "${BLUE}Deploying files...${NC}"
rsync -avz --delete \
    --exclude 'node_modules' \
    --exclude '.env' \
    --exclude 'logs' \
    --exclude '.git' \
    --exclude 'tmp' \
    $LOCAL_PATH/ $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/

if [ $? -ne 0 ]; then
    echo -e "${RED}Deployment failed!${NC}"
    exit 1
fi

# 3. Install dependencies and run migrations
echo -e "${BLUE}Setting up production environment...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    cd $REMOTE_PATH

    # Install dependencies
    npm ci --production

    # Run database migrations
    NODE_ENV=production node scripts/migrate.js

    # Start/restart the application
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

    # Set proper permissions
    chmod -R 755 .
    find . -type f -exec chmod 644 {} \;
    chmod 600 .env
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Setup failed! Rolling back...${NC}"
    ssh $REMOTE_USER@$REMOTE_HOST "
        cd $REMOTE_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/backup_$TIMESTAMP.tar.gz -C $REMOTE_PATH
        npm ci --production
        pm2 reload api-docmatrix
    "
    exit 1
fi

# 4. Verify deployment
echo -e "${BLUE}Verifying deployment...${NC}"
sleep 5 # Wait for the server to start

HEALTH_CHECK=$(curl -s https://api.docmatrixai.com/health)
if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo -e "${GREEN}Deployment successful!${NC}"
    echo -e "${GREEN}API is running and healthy${NC}"
else
    echo -e "${RED}Deployment verification failed!${NC}"
    echo -e "${RED}Rolling back...${NC}"
    ssh $REMOTE_USER@$REMOTE_HOST "
        cd $REMOTE_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/backup_$TIMESTAMP.tar.gz -C $REMOTE_PATH
        npm ci --production
        pm2 reload api-docmatrix
    "
    exit 1
fi

# 5. Clean up old backups (keep last 7 days)
echo -e "${BLUE}Cleaning up old backups...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    find $BACKUP_PATH -type f -mtime +7 -name 'backup_*.tar.gz' -delete
"

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "You can monitor the application using:"
echo -e "  - Health check: https://api.docmatrixai.com/health"
echo -e "  - Logs: tail -f /home1/ixkhjgte/logs/api-*.log"
echo -e "  - PM2: pm2 monit"
