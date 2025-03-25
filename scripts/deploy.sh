#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Hostgator SSH Configuration
DEPLOY_USER="ixkhjgte"
DEPLOY_HOST="docmatrixai.com"
DEPLOY_KEY="~/.ssh/docmatrix_prod_deploy"
REMOTE_PATH="/home1/ixkhjgte/public_html"
API_PATH="${REMOTE_PATH}/api"
WEB_PATH="${REMOTE_PATH}"

# Backup function
backup_remote() {
    echo -e "${BLUE}Creating backup...${NC}"
    ssh -i $DEPLOY_KEY $DEPLOY_USER@$DEPLOY_HOST "cd $REMOTE_PATH && \
        tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz public_html/ && \
        mv backup-*.tar.gz backups/"
}

# Deploy function
deploy() {
    echo -e "${BLUE}Deploying to production...${NC}"
    
    # Sync API files
    rsync -avz --delete \
        -e "ssh -i $DEPLOY_KEY" \
        --exclude 'node_modules' \
        --exclude '.env' \
        --exclude 'logs' \
        --exclude 'uploads' \
        --exclude '.git' \
        ./API/ \
        $DEPLOY_USER@$DEPLOY_HOST:$API_PATH/

    # Sync Web files
    rsync -avz --delete \
        -e "ssh -i $DEPLOY_KEY" \
        --exclude 'node_modules' \
        --exclude '.env' \
        --exclude '.next' \
        --exclude '.git' \
        ./docmatrixai_com/ \
        $DEPLOY_USER@$DEPLOY_HOST:$WEB_PATH/

    # Set permissions
    ssh -i $DEPLOY_KEY $DEPLOY_USER@$DEPLOY_HOST "cd $REMOTE_PATH && \
        find . -type f -exec chmod 644 {} \; && \
        find . -type d -exec chmod 755 {} \; && \
        chmod 755 api/scripts/*.sh && \
        chmod 600 api/.env docmatrixai_com/.env"
}

# Verify deployment
verify() {
    echo -e "${BLUE}Verifying deployment...${NC}"
    
    # Check API health
    API_HEALTH=$(curl -s https://api.docmatrixai.com/health)
    if [[ $API_HEALTH == *"healthy"* ]]; then
        echo -e "${GREEN}API is healthy${NC}"
    else
        echo -e "${RED}API health check failed${NC}"
    fi

    # Check website
    WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://docmatrixai.com)
    if [[ $WEB_STATUS == "200" ]]; then
        echo -e "${GREEN}Website is up${NC}"
    else
        echo -e "${RED}Website check failed${NC}"
    fi
}

# Main deployment process
echo -e "${BLUE}Starting deployment process...${NC}"

# 1. Create backup
backup_remote

# 2. Deploy code
deploy

# 3. Verify deployment
verify

echo -e "${GREEN}Deployment complete!${NC}"
