from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from .models import ChatGroup, GroupMessage
from .serializers import MessageSerializer

User = get_user_model()


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def group_messages(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    if request.method == "GET":
        messages = group.chat_messages.order_by("created")[:50]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        body = request.data.get("body", "")
        file = request.FILES.get("file")
        msg = GroupMessage.objects.create(group=group, author=request.user, body=body, file=file)

       
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{group_name}",
            {
                "type": "chat_message",
                "author": request.user.username,
                "message": msg.body,
                "message_id": msg.id,
                "file": msg.file.url if msg.file else None,
                "created": msg.created.isoformat(),
            },
        )

        serializer = MessageSerializer(msg)
        return Response(serializer.data, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_file_upload(request, chatroom_name):
    group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    file = request.FILES.get("file")
    if file:
        msg = GroupMessage.objects.create(group=group, author=request.user, file=file)
        return Response({"id": msg.id, "file": msg.file.url})
    return Response({"error": "No file"}, status=400)
