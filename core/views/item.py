from rest_framework.viewsets import ModelViewSet

from core.models import Item, Categoria 
from core.serializers import ItemSerializer, CategoriaSerializer

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer    