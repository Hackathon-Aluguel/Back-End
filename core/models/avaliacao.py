from django.db import models
from core.models import User
#from .models import Item

class avaliacao_User (models.Model):
    descricao = models.CharField(max_length=45)
    estrelas = models.DecimalField(max_digits=1, decimal_places=1)
    avaliado = models.ForeignKey(User, on_delete=models.PROTECT)
    avaliador = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'User avaliado: {self.avaliado}, Avaliador: {self.avaliador}'

class avaliacao_Item (models.Model):
    descricao = models.CharField(max_length=45)
    estrelas = models.DecimalField(max_digits=1, decimal_places=1)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    #item = models.ForeignKey(Item, on_delete=models.PROTECT)

    def __str__(self):
        return f'Usuario: {self.usuario}, Item: {self.item}'