from django.db import models
from core.models import User
from core.models.item import Item

class Aluguel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null= True, blank= True)

    def __str__ (self):
        return f'{self.usuario}'

    class Meta:
        verbose_name = 'Aluguel'
        verbose_name_plural = 'Alugueis'
    
class Item_aluguel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null= True, blank= True)
    aluguel = models.ForeignKey(Aluguel, on_delete=models.PROTECT, null= True, blank= True)
    quantidade = models.IntegerField(default=0)
    data_entrega = models.DateField(null= True, blank= True)
    data_devolucao = models.DateField(null= True, blank= True)

    def __str__ (self):
        return f'{self.item}'

    class Meta:
        verbose_name = 'Item_aluguel'
        verbose_name_plural = 'Itens_aluguel'