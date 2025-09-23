from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from core.models import User, Item_aluguel
from core.serializers.aluguel import Item_aluguelSerializer


class userSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'imagem']

    def get_itens_alugados(self, instance):
        itens = Item_aluguel.objects.filter(aluguel__usuario=instance)
        return Item_aluguelSerializer(itens, many=True).data

    # CADASTRO users

    from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user