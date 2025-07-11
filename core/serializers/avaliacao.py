from rest_framework.serializers import ModelSerializer

from core.models import avaliacao_Item, avaliacao_User

class avaliacao_ItemSerializer(ModelSerializer):
    class Meta:
        model = avaliacao_Item
        fields = '__all__'

class avaliacao_UserSerializer(ModelSerializer):
    class Meta:
        model = avaliacao_User
        fields = '__all__'