from rest_framework.serializers import ModelSerializer

from core.models import Aluguel, Item_aluguel

class AluguelSerializer(ModelSerializer):
    class Meta:
        model = Aluguel
        fields = '__all__'

class Item_aluguelSerializer(ModelSerializer):
    class Meta:
        model = Item_aluguel
        fields = '__all__'