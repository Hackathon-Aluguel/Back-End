from django.db import models
from core.models.user import User

import os
import uuid

class Categoria (models.Model):
    descricao = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.descricao}'


class Condicao (models.Model):
    descricao = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.descricao}'

def image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1] 
    filename = f"{uuid.uuid4()}{ext}"
    return f'images/users/{filename}'

class Item (models.Model):
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=45)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_limite = models.DateField()
    categoria = models.ForeignKey (Categoria, on_delete=models.PROTECT, blank=True, null=True)
    usuario = models.ForeignKey (User, on_delete=models.PROTECT, blank=True, null= True)
    numero = models.CharField(max_length=10, blank=True, null=True, help_text=('Numero da casa do usuario.'))
    nome_rua = models.CharField(max_length=10, blank=True, null=True, help_text=('Nome da rua do usuario.'))
    condicao = models.ForeignKey (Condicao, on_delete=models.PROTECT, blank=True, null= True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    quant_estoque = models.IntegerField(default=0)

    def __str__(self):
        return f'Item: {self.nome}'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    def __str__(self):
        return f'Item: {self.nome}'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

    
