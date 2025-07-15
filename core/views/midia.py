from rest_framework.viewsets import ModelViewSet
from core.models.midia import Midia, Midia_item
from core.serializers.midia import MidiaSerializer, Midia_itemSerializer


class MidiaViewSet(ModelViewSet):
    queryset = Midia.objects.all()
    serializer_class = MidiaSerializer

class Midia_itemViewSet(ModelViewSet):
    queryset = Midia_item.objects.all()
    serializer_class = Midia_itemSerializer


