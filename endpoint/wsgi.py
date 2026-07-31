"""
WSGI config for endpoint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endpoint.settings')

application = get_wsgi_application()
