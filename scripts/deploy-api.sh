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
LOCAL_PATH="./api.docmatrixai.com"
BACKUP_PATH="/home1/ixkhjgte/backups/api"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${BLUE}Starting API deployment...${NC}"

# Create backup
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

# Deploy files
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

# Install dependencies and rebuild
echo -e "${BLUE}Installing dependencies...${NC}"
ssh $REMOTE_USER@$REMOTE_HOST "
    cd $REMOTE_PATH
    npm ci --production
    npm rebuild
    pm2 restart api-docmatrix
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Dependency installation failed!${NC}"
    exit 1
fi

# Verify deployment
echo -e "${BLUE}Verifying deployment...${NC}"
HEALTH_CHECK=$(curl -s https://api.docmatrixai.com/health)
if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo -e "${GREEN}Deployment successful!${NC}"
else
    echo -e "${RED}Deployment verification failed!${NC}"
    echo -e "${RED}Rolling back...${NC}"
    ssh $REMOTE_USER@$REMOTE_HOST "
        cd $REMOTE_PATH
        rm -rf *
        tar -xzf $BACKUP_PATH/backup_$TIMESTAMP.tar.gz -C $REMOTE_PATH
        pm2 restart api-docmatrix
    "
    exit 1
fi

echo -e "${GREEN}API deployment completed successfully!${NC}"
