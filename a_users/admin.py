from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'cpf', 'imagem', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'cpf', 'imagem', 'role', 'is_active', 'is_staff', 'is_superuser')

