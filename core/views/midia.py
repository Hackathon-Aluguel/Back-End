from rest_framework.viewsets import ModelViewSet
from core.models import Midia, Midia_itens
from core.serializers import MidiaSerializer, Midia_itensSerializer


class MidiaViewSet(ModelViewSet):
    queryset = Midia.objects.all()
    serializer_class = MidiaSerializer

class Midia_itensViewSet(ModelViewSet):
    queryset = Midia_itens.objects.all()
    serializer_class = Midia_itensSerializer


