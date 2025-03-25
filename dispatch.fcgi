#!/home/USERNAME/public_html/expense-doc/venv/bin/python
import os
import sys

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'expense_doc.settings'

# Create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Run the FastCGI server
from flup.server.fcgi import WSGIServer
WSGIServer(application).run() 