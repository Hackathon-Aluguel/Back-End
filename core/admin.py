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


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'cpf','role',
                    'imagem',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)