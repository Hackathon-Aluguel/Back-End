from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

import mimetypes
import uuid
import os

def image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1] 
    filename = f"{uuid.uuid4()}{ext}"
    return f'images/users/{filename}'

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('padrao', 'Padrão'),
    )
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('email'), help_text=_('Email'))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('name'), help_text=_('Username'))
    cpf = models.CharField(max_length=11, default=None, null=True, help_text=_('CPF do usuário'))

    #midia = models.ForeignKey('core.Midia', on_delete=models.PROTECT, blank=True, null=True)
    imagem = models.ImageField(upload_to=image_file_path, null=True, blank=True)

    is_active = models.BooleanField(
        default=True, verbose_name=_('Usuário está ativo'), help_text=_('Indica que este usuário está ativo.')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='padrao')
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Usuário é da equipe'),
        help_text=_('Indica que este usuário pode acessar o Admin.'),
    )

    objects = UserManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'