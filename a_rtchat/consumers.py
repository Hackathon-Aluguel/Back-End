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

    # Receber mensagem do WebSocket
    class ChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f"chat_{self.room_name}"

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
        """
        Caso você queira permitir envio direto pelo WS (sem REST).
        Eu recomendo usar só REST + broadcast, mas deixo aqui.
        """
        data = json.loads(text_data)
        message = data.get("message", "")

        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            return  # ignora se não autenticado

        group = await database_sync_to_async(ChatGroup.objects.get)(group_name=self.room_name)
        msg = await database_sync_to_async(GroupMessage.objects.create)(
            group=group, author=user, body=message
        )

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
        """
        Broadcast final enviado para os clientes conectados.
        """
        await self.send(text_data=json.dumps({
            "author": event["author"],
            "message": event["message"],
            "file": event.get("file"),
            "message_id": event["message_id"],
            "created": event["created"]
        }))

@database_sync_to_async
def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

@database_sync_to_async
def save_message(self, user, chatroom_name, message):
        group = ChatGroup.objects.get(group_name=chatroom_name)
        return GroupMessage.objects.create(group=group, author=user, body=message)


def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=json.dumps({'type': 'message', 'html': html}))

def update_online_count(self):
        online_count = self.chatroom.users_online.count()
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string("a_rtchat/partials/online_count.html", {'online_count': online_count})
        self.send(text_data=json.dumps({'type': 'online_count', 'html': html}))
