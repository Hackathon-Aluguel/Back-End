from django.urls import re_path
from . import consumers
from .consumers import *

websocket_urlpatterns = [
    re_path(r"ws/chatroom/(?P<chatroom_name>[\w-]+)/$", consumers.ChatroomConsumer.as_asgi()),
]