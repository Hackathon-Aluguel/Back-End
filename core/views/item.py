# core/views/item.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Item, Categoria, Midia, Midia_item
from core.serializers import ItemSerializer, CategoriaSerializer
from rest_framework.permissions import AllowAny

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        fotos = request.FILES.getlist('fotos')
        if fotos:
            midias = []
            for foto in fotos:
                midia = Midia.objects.create(file=foto, descricao='Foto do produto')
                midias.append(midia)
            midia_item = Midia_item.objects.create(item=item)
            midia_item.midia.add(*midias)  # adiciona todas as mídias
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
