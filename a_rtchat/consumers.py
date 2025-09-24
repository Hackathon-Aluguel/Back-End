# path: a_rtchat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from .models import ChatGroup, GroupMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # room_name vem da rota: ws/chatroom/<room_name>/
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope.get("user")
        # se não autenticado, recusamos
        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        # junta o canal ao grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Espera JSON com { message: "texto" }
        Salva no banco e broadcast para o grupo.
        """
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
        # NOTE: não lidamos com upload de arquivos via WS aqui.
        # Para arquivos continue usando o endpoint REST que você já tem.

        # salva no banco (sync -> async wrapper)
        msg = await self._save_message(user, message)

        # envia para o grupo (payload consistente com front)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # mapeado para self.chat_message
                "id": msg.id,
                "author": msg.author.username,
                "message": msg.body,
                "file": msg.file.url if msg.file else None,
                "created": msg.created.isoformat(),
            },
        )

    async def chat_message(self, event):
        """
        Envia o evento para o cliente WS (JSON).
        """
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def _save_message(self, user, body):
        """
        Garante que o ChatGroup exista (útil em dev) e cria a mensagem.
        """
        group, _ = ChatGroup.objects.get_or_create(group_name=self.room_name)
        return GroupMessage.objects.create(group=group, author=user, body=body)
