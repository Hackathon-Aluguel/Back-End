from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import User, Item_aluguel
from core.serializers.aluguel import Item_aluguelSerializer


class userSerializer(ModelSerializer):
    itens_alugados = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'cpf', 'role', 'imagem', 'itens_alugados']

    def get_itens_alugados(self, instance):
        itens = Item_aluguel.objects.filter(aluguel__usuario=instance)
        return Item_aluguelSerializer(itens, many=True).data