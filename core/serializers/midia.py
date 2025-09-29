from rest_framework import serializers
from core.models import Midia, Midia_item

class MidiaSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='url', read_only=True)  # usa a property do modelo

    class Meta:
        model = Midia
        fields = ['id', 'descricao', 'url']  # só enviamos a URL pública

class MidiaItemSerializer(serializers.ModelSerializer):
    midia = MidiaSerializer(many=True, read_only=True)  # garante que o ItemSerializer pegue as imagens

    class Meta:
        model = Midia_item
        fields = ['id', 'item', 'midia']
