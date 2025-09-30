from django.contrib import admin

from core.models.avaliacao import avaliacao_Item, avaliacao_User
from core.models.item import Item, Categoria
from core.models.aluguel import Aluguel, Item_aluguel
from core.models.midia import Midia, Midia_item

admin.site.register(avaliacao_Item)
admin.site.register(avaliacao_User)
admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Aluguel)
admin.site.register(Item_aluguel)
admin.site.register(Midia)
admin.site.register(Midia_item)


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from a_users.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'cpf', 'imagem', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'cpf', 'imagem', 'role', 'is_active', 'is_staff', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('id', 'email', 'username', 'cpf', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('username', 'cpf', 'imagem', 'role')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'cpf', 'imagem', 'role', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

    search_fields = ('email', 'username', 'cpf')
    ordering = ('email',)


admin.site.register(User, UserAdmin)