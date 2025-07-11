from django.db import models 
from core.models.item import Item

class Midia (models.Model):
    nome = models.CharField(max_length=45)
    chave_midia = models.CharField(max_length=45)
    
    def __str__(self):
        return f'Chave: {self.chave_midia}'
    

class Midia_itens(models.Model):
   item = models.ForeignKey(Item, on_delete=models.PROTECT)
   midia = models.ManyToManyField(Midia, related_name="Midia", blank=True)

   def __str__(self):
       return f'Item: ${self.midia} - Midia: {self.midia}'
   
   
