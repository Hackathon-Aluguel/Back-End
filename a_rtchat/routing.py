# a_rtchat/routing.py
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from a_rtchat.middleware import JWTAuthMiddleware
from . import consumers

application = ProtocolTypeRouter({
    "websocket": JWTAuthMiddleware(
        URLRouter([
            re_path(r'ws/chatroom/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
        ])
    ),
})
