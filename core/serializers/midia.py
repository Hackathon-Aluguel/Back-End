from rest_framework.serializers import ModelSerializer
from core.models import Midia, Midia_item

class MidiaSerializer(ModelSerializer):
    class Meta:
        model = Midia
        fields = '__all__'

class MidiaItemSerializer(ModelSerializer):
    class Meta:
        model = Midia_item
        fields = '__all__'
