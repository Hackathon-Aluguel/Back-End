from django.db import models

class Categoria (models.Model):
    descricao = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.descricao}'

class Item (models.Model):
    nome = models.CharField(max_length=45)
    descricao = models.CharField(max_length=45)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tempo_limite = models.DateField()
    categoria = models.ForeignKey (Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return f'Item: {self.nome}'

