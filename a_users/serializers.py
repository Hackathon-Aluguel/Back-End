from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    info = serializers.CharField(source='user.info', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'avatar', 'info']