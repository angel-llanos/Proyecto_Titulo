from django import forms
from datetime import datetime, time, timedelta
from .models import Reserva, Zona, Menu

class ReservaForm(forms.ModelForm):
    HORA_INICIO = time(11, 0)
    HORA_CIERRE = time(0, 0)  # medianoche (00:00)
    INTERVALO = timedelta(minutes=15)

    comensales = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 13)],
        initial='1',
        label="Número de comensales",
        widget=forms.Select(attrs={'class': 'form-control select-comensales'})
    )

    hora = forms.ChoiceField(
        label="Hora",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = ['nombre_reserva', 'fecha', 'hora', 'telefono', 'zona', 'menu', 'comensales']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.now().strftime('%Y-%m-%d'),
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zona'].queryset = Zona.objects.all().only('id', 'nombre')
        self.fields['menu'].queryset = Menu.objects.all().only('id', 'nombre')
        self.fields['menu'].required = False

        horas = []
        actual = datetime.combine(datetime.today(), self.HORA_INICIO)
        fin = datetime.combine(datetime.today(), time(0, 0)) + timedelta(days=1)

        while actual < fin:
            hora_texto = actual.strftime('%H:%M')
            horas.append((hora_texto, hora_texto))
            actual += self.INTERVALO

        self.fields['hora'].choices = horas

        if not self.is_bound:
            now = datetime.now()
            minute = ((now.minute + 14) // 15) * 15
            now = now.replace(second=0, microsecond=0)

            if minute == 60:
                if now.hour == 23:
                    now = now.replace(hour=0, minute=0) + timedelta(days=1)
                else:
                    now = now.replace(hour=now.hour + 1, minute=0)
            else:
                now = now.replace(minute=minute)

            if now.time() < self.HORA_INICIO:
                now = now.replace(hour=11, minute=0)
            elif now.time() < time(11, 0) or now.time() >= time(0, 0) and now.time() < self.HORA_INICIO:
                now = datetime.combine(now.date() + timedelta(days=1), self.HORA_INICIO)

            self.initial['fecha'] = now.date()
            self.initial['hora'] = now.strftime('%H:%M')


    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        zona = cleaned_data.get('zona')

        if not all([fecha, hora, zona]):
            return cleaned_data

        now = datetime.now()

        if fecha < now.date():
            self.add_error('fecha', "No puedes reservar en fechas pasadas.")

        #validación segura del tiempo
        try:
            hora_time = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            self.add_error('hora', "Formato de hora inválido.")
            return cleaned_data

        #valida que esté dentro del rango
        if not (time(11, 0) <= hora_time or hora_time == time(0, 0)):
            self.add_error('hora', "El horario de reserva es entre 11:00 y 00:00.")

        #validar múltiplos de 15 minutos (sólo por si acaso)
        if hora_time.minute % 15 != 0:
            self.add_error('hora', "Selecciona una hora con intervalo de 15 minutos.")

        return cleaned_data
