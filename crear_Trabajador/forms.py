from django import forms
from registrar.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CrearTrabajadorForm(forms.ModelForm):
    ROL_CHOICES_LIMITED = (
        (2, 'Trabajador'),
        (3, 'Cocinero'),
    )

    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)
    username = forms.CharField(label='Nombre de usuario', required=True)
    email = forms.EmailField(label='Correo electrónico', required=True)

    rol = forms.ChoiceField(
        choices=ROL_CHOICES_LIMITED,
        label="Rol del nuevo usuario",
        required=True
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        required=True
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'rol']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Validación de que las contraseñas coincidan
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Las contraseñas no coinciden")

            # Validación de fortaleza de la contraseña
            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error('password1', e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
