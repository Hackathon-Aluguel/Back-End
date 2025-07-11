from rest_framework.serializers import ModelSerializer

from core.models import Item, Categoria

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
