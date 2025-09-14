# core/views/item.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Item, Categoria, Midia, Midia_item
from core.serializers import ItemSerializer, CategoriaSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Item, com suporte a múltiplas imagens.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        # 1️⃣ Cria o item
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        # 2️⃣ Processa as fotos enviadas
        fotos = request.FILES.getlist('fotos')
        if fotos:
            midias = []
            for foto in fotos:
                midia = Midia.objects.create(file=foto, descricao='Foto do produto')
                midias.append(midia)

            # 3️⃣ Cria o Midia_item e associa as mídias
            midia_item = Midia_item.objects.create(item=item)
            midia_item.midia.add(*midias)  # adiciona todas as mídias

        # 4️⃣ Retorna a resposta
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Categoria.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
