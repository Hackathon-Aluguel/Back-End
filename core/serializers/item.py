from rest_framework import serializers
from core.models import Item, Categoria, Midia, Midia_item

class MidiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Midia
        fields = ['id', 'descricao', 'file', 'url']

class ItemSerializer(serializers.ModelSerializer):
    fotos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    midias = MidiaSerializer(source='midia_item.midia', many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'nome', 'descricao', 'preco', 'tempo_limite',
                  'numero', 'nome_rua', 'categoria', 'usuario', 'condicao',
                  'cor', 'quant_estoque', 'midias', 'fotos']
        read_only_fields = ['usuario']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        fotos_data = validated_data.pop('fotos', [])
        item = Item.objects.create(usuario=user, **validated_data)
        midia_item, created = Midia_item.objects.get_or_create(item=item)
        for foto in fotos_data:
            midia = Midia.objects.create(file=foto)
            midia_item.midia.add(midia)
        return item


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
