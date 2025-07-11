from rest_framework.serializers import ModelSerializer
from core.models import Midia, Midia_itens


class MidiaSerializer(ModelSerializer):
    class Meta: 
        model = Midia
        fields = '_all_'


class Midia_itensSerializer(ModelSerializer):
    class Meta:
        model = Midia_itens
        fields = '_all_'        


