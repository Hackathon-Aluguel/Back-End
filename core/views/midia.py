from rest_framework.viewsets import ModelViewSet
from core.models.midia import Midia, Midia_item
from core.serializers.midia import MidiaSerializer, Midia_itemSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MidiaViewSet(ModelViewSet):
    queryset = Midia.objects.all()
    serializer_class = MidiaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class Midia_itemViewSet(ModelViewSet):
    queryset = Midia_item.objects.all()
    serializer_class = Midia_itemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        item = serializer.validated_data.get("item")
        if item.usuario != self.request.user:
            raise PermissionDenied("Você não pode adicionar mídia a itens de outro usuário.")
        serializer.save()


