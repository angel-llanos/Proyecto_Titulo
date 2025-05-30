from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        }