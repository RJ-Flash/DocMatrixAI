#!/usr/bin/env python

import os
import sys
from pathlib import Path

# Add the project directory to the sys.path
current_dir = Path(__file__).resolve().parent
project_dir = current_dir / 'expense_doc'
sys.path.append(str(current_dir))
sys.path.append(str(project_dir))

# Set up Django's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'expense_doc.settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false") 