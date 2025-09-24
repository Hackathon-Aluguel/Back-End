from django.urls import path
from . import views

urlpatterns = [
    path("api/chat/<str:group_name>/messages/", views.group_messages, name="group_messages"),
]
