from rest_framework import serializers
from .models import GroupMessage

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        model = GroupMessage
        fields = ['id', 'author', 'body', 'file', 'created']
