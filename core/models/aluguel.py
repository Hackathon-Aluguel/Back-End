from django.db import models
from core.models import User
from core.models.item import Item

class Aluguel(models.Model):
    data_entrega = models.DateField(null= True, blank= True)
    data_devolucao = models.DateField(null= True, blank= True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null= True, blank= True)

    def _str_ (self):
        return f'{self.usuario}'
    
class Item_aluguel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null= True, blank= True)
    aluguel = models.ForeignKey(Aluguel, on_delete=models.PROTECT, null= True, blank= True)
    quantidade = models.IntegerField(default=0)

    def _str_ (self):
        return f'{self.item}'

    class Meta:
        verbose_name = 'Item_aluguel'
        verbose_name_plural = 'Itens_aluguel'