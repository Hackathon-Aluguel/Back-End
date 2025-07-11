from rest_framework.viewsets import ModelViewSet
from core.models.avaliacao import avaliacao_Item, avaliacao_User
from core.serializers.avaliacao import avaliacao_ItemSerializer, avaliacao_UserSerializer

class avaliacao_ItemViewSet(ModelViewSet):
    queryset = avaliacao_Item.objects.all()
    serializer_class = avaliacao_ItemSerializer

class avaliacao_UserViewSet(ModelViewSet):
    queryset = avaliacao_User.objects.all()
    serializer_class = avaliacao_UserSerializer