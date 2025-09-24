from rest_framework import serializers
from .models import GroupMessage

class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = GroupMessage
        fields = ["id", "author_username", "body", "file", "created"]
