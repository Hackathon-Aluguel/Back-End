# path: a_rtchat/models.py
from django.db import models
from django.conf import settings
import shortuuid

User = settings.AUTH_USER_MODEL

def generate_short_id():
    return shortuuid.ShortUUID().random(length=12)

class PrivateChat(models.Model):
    """
    Conversa privada entre exatamente (até) 2 usuários.
    chat_id: string única (shortuuid) usada nas URLs/ws.
    participants: ManyToMany, aplicamos controle de negócios para 2 participantes.
    """
    chat_id = models.CharField(max_length=32, unique=True, default=generate_short_id, editable=False)
    participants = models.ManyToManyField(User, related_name="private_chats")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PrivateChat {self.chat_id} ({self.participants.count()} participants)"

    def has_participant(self, user):
        return self.participants.filter(pk=getattr(user, "pk", None)).exists()


class GroupMessage(models.Model):
    """
    Mensagem linkada a PrivateChat (campo 'group' renomeado para 'chat' para evitar confusão).
    Mantive o nome GroupMessage para compatibilidade com seu código existente.
    """
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name="chat_messages", default="", null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(default="", blank=True)
    file = models.FileField(upload_to="chat_files/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.author} - {self.body[:30]}"
