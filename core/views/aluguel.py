from rest_framework.viewsets import ModelViewSet
from core.models.aluguel import Aluguel, Item_aluguel
from core.serializers.aluguel import AluguelSerializer, Item_aluguelSerializer

from rest_framework.permissions import IsAuthenticated

from core.permissions.roles import IsAdmin, IsPadrao


class AluguelViewSet(ModelViewSet):
    queryset = Aluguel.objects.all()
    serializer_class = AluguelSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Aluguel.objects.all()
        elif user.role == 'padrao':
            return Aluguel.objects.filter(usuario=user)
        return Aluguel.objects.none()

class Item_aluguelViewSet(ModelViewSet):
    queryset = Item_aluguel.objects.all()
    serializer_class = Item_aluguelSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Item_aluguel.objects.all()
        elif user.role == 'padrao':
            return Item_aluguel.objects.filter(aluguel__usuario=user)
        return Item_aluguel.objects.none()
