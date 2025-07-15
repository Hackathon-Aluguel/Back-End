from django.db import models 
from core.models.item import Item

'''class Midia (models.Model):
    nome = models.CharField(max_length=45)
    chave_midia = models.CharField(max_length=45)
    
    def __str__(self):
        return f'Chave: {self.chave_midia}'''

import mimetypes
import uuid

from django.db import models


def image_file_path(image, _) -> str:
    extension: str = mimetypes.guess_extension(image.file.file.content_type)
    if extension == '.jpe':
        extension = '.jpg'
    return f'images/{image.public_id}{extension or ""}'

class Midia(models.Model):
    attachment_key = models.UUIDField(
        max_length=255,
        default=uuid.uuid4,
        unique=True,
        help_text=('Used to attach the image to another object. Cannot be used to retrieve the image file.'),
    )
    public_id = models.UUIDField(
        max_length=255,
        default=uuid.uuid4,
        unique=True,
        help_text=(
            'Used to retrieve the image itself. Should not be readable until the image is attached to another object.'
        ),
    )
    file = models.ImageField(upload_to=image_file_path)
    descricao = models.CharField(max_length=255, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Midia: {self.descricao} - {self.attachment_key}'

    @property
    def url(self) -> str:
        return self.file.url  # pylint: disable=no-member
    

class Midia_item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    midia = models.ManyToManyField(Midia, related_name="Midia", blank=True)

    def __str__(self):
        descricoes = ", ".join([m.descricao for m in self.midia.all()])
        return f'{self.item} - Midias: {descricoes}'

    class Meta:
        verbose_name = 'Midia_item'
        verbose_name_plural = 'Midias_item'

    
       
    
   
   
