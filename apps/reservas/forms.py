from django import forms
from .models import Reserva, Zona, Menu

class ReservaForm(forms.ModelForm):
    zona = forms.ModelChoiceField(queryset=Zona.objects.all(), required=True)
    menu = forms.ModelChoiceField(queryset=Menu.objects.all(), required=False)
    comensales = forms.IntegerField(min_value=1, initial=1, label="Número de comensales")

    class Meta:
        model = Reserva
        fields = ['nombre_reserva', 'fecha', 'hora', 'telefono', 'zona', 'menu', 'comensales']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }