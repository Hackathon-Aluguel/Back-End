# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ASGI app do Django (HTTP)
application = get_asgi_application()

