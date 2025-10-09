# path: a_rtchat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("api/chats/", views.list_my_chats, name="list_my_chats"),  # lista do usuário
    path("api/chats/create_or_get/", views.create_or_get_private_chat, name="create_or_get_private_chat"),
    path("api/chats/<str:chat_id>/messages/", views.chat_messages, name="chat_messages"),
]
