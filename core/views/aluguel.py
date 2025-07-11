from rest_framework.viewsets import ModelViewSet
from core.models.aluguel import Aluguel, Item_aluguel
from core.serializers.aluguel import AluguelSerializer, Item_aluguelSerializer

class AluguelViewSet(ModelViewSet):
    queryset = Aluguel.objects.all()
    serializer_class = AluguelSerializer

class Item_aluguelViewSet(ModelViewSet):
    queryset = Item_aluguel.objects.all()
    serializer_class = Item_aluguelSerializer