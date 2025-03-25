Installation Guide
=================

This guide will help you install and set up ExpenseDocAI in your environment.

System Requirements
-----------------

* Python 3.9 or higher
* MySQL 8.0 or higher
* Redis 6.0 or higher
* 4GB RAM minimum (8GB recommended)
* 20GB disk space
* Windows 10/11, macOS 10.15+, or Linux

Prerequisites
------------

Before installing ExpenseDocAI, ensure you have the following tools installed:

1. Python 3.9+
2. pip (Python package installer)
3. Git
4. MySQL Server
5. Redis Server

Installation Steps
----------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/docmatrixai/expensedocai.git
   cd expensedocai

2. Create Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate

3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt
   # For development
   pip install -r requirements-dev.txt

4. Configure Environment
~~~~~~~~~~~~~~~~~~~~~~

Copy the example environment file and update it with your settings:

.. code-block:: bash

   cp .env.example .env

Edit the `.env` file with your database credentials and other settings.

5. Initialize Database
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py migrate
   python manage.py createsuperuser

6. Collect Static Files
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py collectstatic

7. Start Development Server
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python manage.py runserver

The application should now be running at http://localhost:8000

Production Deployment
-------------------

For production deployment, additional steps are required:

1. Set Debug Mode
~~~~~~~~~~~~~~~

In your `.env` file, set:

.. code-block:: bash

   DJANGO_DEBUG=False
   ALLOWED_HOSTS=your-domain.com

2. Configure Web Server
~~~~~~~~~~~~~~~~~~~~

Set up a web server (e.g., Nginx) to serve the application:

.. code-block:: nginx

   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /path/to/your/static/;
       }
       
       location /media/ {
           alias /path/to/your/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }

3. Set Up SSL
~~~~~~~~~~~~

Configure SSL certificates for secure HTTPS connections.

4. Configure Process Manager
~~~~~~~~~~~~~~~~~~~~~~~~~

Set up a process manager like supervisord to manage the application:

.. code-block:: ini

   [program:expensedocai]
   command=/path/to/venv/bin/gunicorn expense_doc.wsgi:application
   directory=/path/to/project
   user=www-data
   autostart=true
   autorestart=true
   redirect_stderr=true

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~

1. Database Connection Issues
   
   * Verify database credentials in `.env`
   * Ensure MySQL server is running
   * Check database user permissions

2. Static Files Not Loading
   
   * Run `collectstatic` command
   * Check web server configuration
   * Verify static root path

3. Permission Errors
   
   * Check file permissions
   * Verify user permissions
   * Ensure correct ownership of files

Getting Help
-----------

If you encounter any issues during installation:

1. Check our `FAQ <https://docs.docmatrixai.com/faq>`_
2. Search existing issues on GitHub
3. Contact our support team
4. Join our community Discord server

Next Steps
---------

After installation, proceed to:

* :doc:`configuration` for detailed configuration options
* :doc:`quickstart` for a quick introduction to using ExpenseDocAI
* :doc:`development/setup` for setting up a development environment 