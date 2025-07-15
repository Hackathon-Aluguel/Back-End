from django.db import models
from core.models import User
from core.models.item import Item
from django.core.validators import MinValueValidator, MaxValueValidator

class avaliacao_User (models.Model):
    descricao = models.CharField(max_length=45)
    estrelas = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    avaliado = models.ForeignKey(User, on_delete=models.PROTECT, related_name="avaliado")
    avaliador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="avaliador")

    def __str__(self):
        return f'User avaliado: {self.avaliado}, Avaliador: {self.avaliador}'

class avaliacao_Item (models.Model):
    descricao = models.CharField(max_length=45)
    estrelas = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'Usuario: {self.usuario}, Item: {self.item}'