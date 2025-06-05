from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  #modelo personalizado de usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()

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
        user.rol = 1 #cliente (1) por defecto
        if commit:
            user.save()
        return user
    

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo no está registrado.")
        return email

    def save(self, **kwargs):
        #crear el PasswordResetForm con los datos validados
        actual_form = PasswordResetForm(data=self.cleaned_data)
        
        #validar el formulario para asegurar que 'cleaned_data' esté disponible
        if actual_form.is_valid():
            return actual_form.save(**kwargs)
        else:
            return actual_form  #en caso de que el formulario no sea válido, se devuelve