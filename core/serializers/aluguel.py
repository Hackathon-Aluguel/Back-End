from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Aluguel, Item_aluguel

total = SerializerMethodField()

class AluguelSerializer(ModelSerializer):
    total = SerializerMethodField()
    quantidade_itens = SerializerMethodField()

    class Meta:
        model = Aluguel
        fields = ['id', 'usuario', 'quantidade_itens', 'total']

    def get_total(self, instance):
        itens = Item_aluguel.objects.filter(aluguel=instance)
        total = 0
        for item in itens:
            if item.data_entrega and item.data_devolucao:
                dias = (item.data_devolucao - item.data_entrega).days
            else:
                dias = 0
            total += item.quantidade * item.item.preco * dias
        return total

    def get_quantidade_itens(self, instance):
        itens = Item_aluguel.objects.filter(aluguel=instance)
        return sum(item.quantidade for item in itens)
    
class Item_aluguelSerializer(ModelSerializer):
    total = SerializerMethodField()
    total_dias = SerializerMethodField()

    class Meta:
        model = Item_aluguel
        fields = ["item", "aluguel", "quantidade", "total", 'total_dias']

    def get_total_dias(self, instance):
        if instance.data_entrega and instance.data_devolucao:
            return (instance.data_devolucao - instance.data_entrega).days
        return 0

    def get_total(self, instance):
        if instance.data_entrega and instance.data_devolucao:
            dias = (instance.data_devolucao - instance.data_entrega).days
        else:
            dias = 0

        return instance.quantidade * instance.item.preco * dias