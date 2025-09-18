# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from a_rtchat.middleware import JWTAuthMiddleware
from a_rtchat import consumers
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ASGI app do Django (HTTP)
django_asgi_app = get_asgi_application()

# Roteamento de WebSocket
websocket_urlpatterns = [
    re_path(r'ws/chatroom/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]

# Aplicação ASGI final
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
