# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # ahora usamos el modelo que creaste

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=30, required=True)
    last_name = forms.CharField(label='Apellido', max_length=30, required=True)
    email = forms.EmailField(label='Correo electrónico', required=True)
    username = forms.CharField(label='Nombre de usuario', max_length=150)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 1  # Cliente por defecto
        if commit:
            user.save()
        return user