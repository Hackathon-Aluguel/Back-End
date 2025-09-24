from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="chat_messages")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(default="", blank=True)
    file = models.FileField(upload_to="chat_files/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.author} - {self.body[:30]}"
