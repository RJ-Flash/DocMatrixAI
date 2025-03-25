#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Hostgator cPanel Configuration
CPANEL_USER="ixkhjgte"
CPANEL_DOMAIN="docmatrixai.com"
BACKUP_EMAIL="admin@docmatrixai.com"

# Backup Paths
BACKUP_ROOT="/home1/ixkhjgte/backups"
DB_BACKUP_PATH="${BACKUP_ROOT}/databases"
FILES_BACKUP_PATH="${BACKUP_ROOT}/files"
LOG_BACKUP_PATH="${BACKUP_ROOT}/logs"

# Create backup directories
echo -e "${BLUE}Creating backup directories...${NC}"
ssh -i ~/.ssh/docmatrix_prod_deploy $CPANEL_USER@$CPANEL_DOMAIN "
    mkdir -p $DB_BACKUP_PATH
    mkdir -p $FILES_BACKUP_PATH
    mkdir -p $LOG_BACKUP_PATH
    chmod 700 $BACKUP_ROOT
"

# Setup database backup cron
echo -e "${BLUE}Setting up database backup cron...${NC}"
ssh -i ~/.ssh/docmatrix_prod_deploy $CPANEL_USER@$CPANEL_DOMAIN "
    echo '0 3 * * * mysqldump -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE | gzip > $DB_BACKUP_PATH/db-backup-\$(date +\%Y\%m\%d).sql.gz' > ~/db_backup_cron
    crontab -l | { cat; cat ~/db_backup_cron; } | crontab -
    rm ~/db_backup_cron
"

# Setup files backup cron
echo -e "${BLUE}Setting up files backup cron...${NC}"
ssh -i ~/.ssh/docmatrix_prod_deploy $CPANEL_USER@$CPANEL_DOMAIN "
    echo '0 2 * * 0 tar -czf $FILES_BACKUP_PATH/files-backup-\$(date +\%Y\%m\%d).tar.gz /home1/ixkhjgte/public_html/' > ~/files_backup_cron
    crontab -l | { cat; cat ~/files_backup_cron; } | crontab -
    rm ~/files_backup_cron
"

# Setup log rotation
echo -e "${BLUE}Setting up log rotation...${NC}"
ssh -i ~/.ssh/docmatrix_prod_deploy $CPANEL_USER@$CPANEL_DOMAIN "
    echo '0 0 * * * find /home1/ixkhjgte/public_html/api/logs -name \"*.log\" -mtime +7 -exec gzip {} \; -exec mv {}.gz $LOG_BACKUP_PATH/ \;' > ~/log_rotation_cron
    crontab -l | { cat; cat ~/log_rotation_cron; } | crontab -
    rm ~/log_rotation_cron
"

# Setup backup cleanup (keep last 30 days)
echo -e "${BLUE}Setting up backup cleanup...${NC}"
ssh -i ~/.ssh/docmatrix_prod_deploy $CPANEL_USER@$CPANEL_DOMAIN "
    echo '0 4 * * * find $BACKUP_ROOT -type f -mtime +30 -delete' > ~/cleanup_cron
    crontab -l | { cat; cat ~/cleanup_cron; } | crontab -
    rm ~/cleanup_cron
"

# Configure backup notifications
echo -e "${BLUE}Setting up backup notifications...${NC}"
ssh -i ~/.ssh/docmatrix_prod_deploy $CPANEL_USER@$CPANEL_DOMAIN "
    echo '0 5 * * * /usr/local/cpanel/bin/backup_report.pl --mail $BACKUP_EMAIL' > ~/notify_cron
    crontab -l | { cat; cat ~/notify_cron; } | crontab -
    rm ~/notify_cron
"

echo -e "${GREEN}Backup configuration complete!${NC}"
echo -e "Backups will run automatically:"
echo -e "- Database: Daily at 3 AM"
echo -e "- Files: Weekly on Sunday at 2 AM"
echo -e "- Logs: Rotated daily at midnight"
echo -e "- Cleanup: Daily at 4 AM (removes backups older than 30 days)"
echo -e "- Notifications: Daily at 5 AM"
echo -e "\nBackup locations:"
echo -e "- Database backups: $DB_BACKUP_PATH"
echo -e "- File backups: $FILES_BACKUP_PATH"
echo -e "- Log backups: $LOG_BACKUP_PATH"
