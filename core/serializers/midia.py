from rest_framework.serializers import ModelSerializer
from core.models.midia import Midia, Midia_item


class MidiaSerializer(ModelSerializer):
    class Meta: 
        model = Midia
        fields = '__all__'


class Midia_itemSerializer(ModelSerializer):
    class Meta:
        model = Midia_item
        fields = '__all__'        


