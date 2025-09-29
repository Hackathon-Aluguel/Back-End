# path: a_rtchat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from .models import ChatGroup, GroupMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope.get("user")
        
        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            return

        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except Exception:
            return

        message = data.get("message", "") or ""
        

       
        msg = await self._save_message(user, message)

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  
                "id": msg.id,
                "author": msg.author.username,
                "message": msg.body,
                "file": msg.file.url if msg.file else None,
                "created": msg.created.isoformat(),
            },
        )

    async def chat_message(self, event):
      
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def _save_message(self, user, body):
       
        group, _ = ChatGroup.objects.get_or_create(group_name=self.room_name)
        return GroupMessage.objects.create(group=group, author=user, body=body)
