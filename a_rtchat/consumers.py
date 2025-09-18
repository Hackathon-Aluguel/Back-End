import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatGroup, GroupMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Entrar no grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        user = self.scope.get("user")
        # ignora mensagens de não autenticados

        group, _ = await database_sync_to_async(ChatGroup.objects.get_or_create)(
            group_name=self.room_name
        )

        msg = await database_sync_to_async(GroupMessage.objects.create)(
            group=group,
            author=user,
            body=message
        )

        # broadcast para todos no grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "author": user.username,
                "message": msg.body,
                "message_id": msg.id,
                "file": msg.file.url if msg.file else None,
                "created": msg.created.isoformat()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "author": event["author"],
            "message": event["message"],
            "file": event.get("file"),
            "message_id": event["message_id"],
            "created": event["created"]
        }))
