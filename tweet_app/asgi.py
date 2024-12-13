"""
ASGI config for tweet_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
# tweet_app/asgi.py

import os
import django
from channels.routing import get_default_application

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweet_app.settings')
django.setup()
application = get_asgi_application()