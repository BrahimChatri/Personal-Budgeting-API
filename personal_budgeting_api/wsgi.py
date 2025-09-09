"""
WSGI config for personal_budgeting_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Set the Django settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_budgeting_api.settings')

# Initialize Django application
application = get_wsgi_application()

# Production WSGI application with WhiteNoise for static files
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'personal_budgeting_api.settings':
    try:
        from whitenoise import WhiteNoise
        application = WhiteNoise(application, root=str(BASE_DIR / 'staticfiles'))
        application.add_files(str(BASE_DIR / 'staticfiles'), prefix='static/')
    except ImportError:
        pass
