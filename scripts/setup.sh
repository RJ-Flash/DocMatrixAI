#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}DocMatrix AI Setup Script${NC}"
echo "================================"

# Check environment
if [ ! -f "project.json" ]; then
    echo -e "${RED}Error: project.json not found${NC}"
    exit 1
fi

# Setup API
echo -e "\n${GREEN}Setting up API...${NC}"
cd API
npm install
npm run create:admin

# Configure IP Whitelist
echo -e "\n${GREEN}Configuring IP Whitelist...${NC}"
npm run whitelist

# Setup Web Frontend
echo -e "\n${GREEN}Setting up Web Frontend...${NC}"
cd ../docmatrixai_com
npm install
npm run build

# Setup SSL Certificates
echo -e "\n${GREEN}Setting up SSL Certificates...${NC}"
certbot certonly --webroot -w ./public \
    -d docmatrixai.com \
    -d api.docmatrixai.com

# Setup Database
echo -e "\n${GREEN}Setting up Database...${NC}"
mysql -u root -p < ./API/config/schema.sql

# Setup Monitoring
echo -e "\n${GREEN}Setting up Monitoring...${NC}"
npm install -g pm2
pm2 start ./API/server.js --name "docmatrix-api"
pm2 start ./docmatrixai_com/server.js --name "docmatrix-web"
pm2 save

echo -e "\n${GREEN}Setup Complete!${NC}"
echo "================================"
echo -e "Next steps:"
echo -e "1. Visit ${BLUE}https://docmatrixai.com/admin${NC} to login"
echo -e "2. Configure additional IP whitelist entries"
echo -e "3. Set up backup schedules"
echo -e "4. Review security settings"
