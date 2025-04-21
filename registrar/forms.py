from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
     first_name = forms.CharField(label='Nombre', max_length=30, required=True)
     last_name = forms.CharField(label='Apellido', max_length=30, required=True)
     email = forms.EmailField(label='Correo electrónico', required=True)
     username = forms.CharField(label='Nombre de usuario', max_length=150)
     
     class Meta:
          model = User
          fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']