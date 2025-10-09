# path: a_rtchat/serializers.py
from rest_framework import serializers
from .models import GroupMessage, PrivateChat

class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = GroupMessage
        fields = ["id", "author_username", "body", "file", "created"]


class PrivateChatSerializer(serializers.ModelSerializer):
    participants_usernames = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChat
        fields = ["chat_id", "participants_usernames", "created", "last_message"]

    def get_participants_usernames(self, obj):
        return [u.username for u in obj.participants.all()]

    def get_last_message(self, obj):
        last = obj.chat_messages.order_by("-created").first()
        if not last:
            return None
        return {
            "id": last.id,
            "author": last.author.username,
            "body": last.body,
            "created": last.created,
        }
