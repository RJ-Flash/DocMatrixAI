# ExpenseDocAI Deployment Guide

This guide provides step-by-step instructions for deploying ExpenseDocAI on HostGator shared hosting.

## Prerequisites

1. HostGator shared hosting account with:
   - Python support enabled
   - MySQL database
   - SSH access

2. Local development environment with:
   - Python 3.9+
   - Git
   - pip

## Deployment Steps

### 1. Database Setup

1. Create a MySQL database in HostGator:
   - Log in to cPanel
   - Navigate to MySQL Databases
   - Create a new database
   - Create a database user
   - Add user to database with all privileges

2. Note down the database credentials:
   - Database name
   - Username
   - Password
   - Host (usually localhost)

### 2. Environment Setup

1. SSH into your HostGator account:
   ```bash
   ssh username@your-domain.com
   ```

2. Create a Python virtual environment:
   ```bash
   cd public_html
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/your-org/expensedocai.git
   cd expensedocai/src
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create and configure .env file:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### 3. Application Configuration

1. Configure the FastCGI wrapper:
   ```bash
   chmod +x dispatch.fcgi
   ```

2. Create .htaccess file in public_html:
   ```apache
   AddHandler fcgid-script .fcgi
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ dispatch.fcgi/$1 [QSA,L]
   ```

3. Configure static files:
   ```bash
   python manage.py collectstatic
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

### 4. Security Configuration

1. Set proper file permissions:
   ```bash
   chmod 750 ~/public_html/expensedocai
   chmod 640 ~/public_html/expensedocai/src/.env
   chmod 750 ~/public_html/expensedocai/src/media
   chmod 750 ~/public_html/expensedocai/src/staticfiles
   ```

2. Configure SSL in cPanel:
   - Install Let's Encrypt SSL certificate
   - Force HTTPS redirection

### 5. Testing the Deployment

1. Test the application:
   ```bash
   # Check the health endpoint
   curl https://your-domain.com/health/
   
   # Test the API
   curl https://your-domain.com/api/v1/documents/
   ```

2. Monitor the error logs:
   ```bash
   tail -f ~/logs/error.log
   ```

### 6. Maintenance

1. Update the application:
   ```bash
   cd ~/public_html/expensedocai
   git pull
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   touch dispatch.fcgi
   ```

2. Backup database regularly:
   ```bash
   # In cPanel:
   # 1. Navigate to Backup Wizard
   # 2. Select "Backup" tab
   # 3. Choose "MySQL Databases"
   # 4. Select your database
   # 5. Download the backup
   ```

### 7. Monitoring

1. Set up error notifications:
   - Configure EMAIL_* settings in .env
   - Add admin emails to ADMINS setting

2. Monitor system resources:
   - Check CPU usage in cPanel
   - Monitor disk space usage
   - Watch database size

### 8. Troubleshooting

1. Application errors:
   - Check ~/logs/error.log
   - Verify permissions
   - Ensure all environment variables are set

2. Database issues:
   - Check MySQL connection
   - Verify database privileges
   - Monitor query performance

3. File upload problems:
   - Check upload_max_filesize in PHP settings
   - Verify media directory permissions
   - Monitor disk space

### 9. Performance Optimization

1. Enable caching:
   ```python
   # In settings.py, ensure cache is configured:
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': get_env_value('REDIS_URL'),
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```

2. Configure static file serving:
   - Enable WhiteNoise compression
   - Set up proper cache headers

3. Optimize database:
   - Create necessary indexes
   - Monitor slow queries
   - Optimize large tables

### 10. Backup Strategy

1. Database backups:
   - Daily automated backups via cPanel
   - Weekly manual backups
   - Store backups off-site

2. File backups:
   - Regular media file backups
   - Configuration file backups
   - Document version control

## Support

For deployment support:
- Email: support@docmatrix.ai
- Documentation: https://docs.docmatrix.ai
- Issue tracker: https://github.com/your-org/expensedocai/issues 