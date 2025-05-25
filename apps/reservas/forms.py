from django import forms
from datetime import datetime, time, timedelta
from .models import Reserva, Zona, Menu

class ReservaForm(forms.ModelForm):
    HORA_INICIO = time(11, 0)  # 11:00 AM
    HORA_CIERRE = time(23, 30)  # 11:30 PM (último turno)
    INTERVALO = timedelta(minutes=30)
    # Cambiamos el IntegerField por un ChoiceField con opciones fijas
    comensales = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 21)],  # De 1 a 20 comensales
        initial='1',
        label="Número de comensales",
        widget=forms.Select(attrs={
            'class': 'form-control select-comensales',
        })
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
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'min': '11:00',
                'max': '23:30',
                'step': '1800',  # 30 minutos en segundos
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimización: Solo traemos los campos necesarios
        self.fields['zona'].queryset = Zona.objects.all().only('id', 'nombre')
        self.fields['menu'].queryset = Menu.objects.all().only('id', 'nombre')
        
        # Establecer hora inicial redondeada a los próximos 30 minutos
        if not self.is_bound:
            now = datetime.now()
            self.initial['fecha'] = now.date()
            
            # Redondeo a la próxima media hora
            if now.minute < 30:
                minute = 30
            else:
                minute = 0
                now = now.replace(hour=now.hour + 1)
            
            # Asegurarnos que no pase de la hora de cierre
            if now.time() > self.HORA_CIERRE:
                now = datetime.combine(now.date() + timedelta(days=1), self.HORA_INICIO)
            
            self.initial['hora'] = now.replace(minute=minute).strftime('%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        zona = cleaned_data.get('zona')

        if not all([fecha, hora, zona]):
            return cleaned_data

        now = datetime.now()
        
        # Validación de fecha
        if fecha < now.date():
            self.add_error('fecha', "No puedes reservar en fechas pasadas.")
        
        # Validación de hora
        hora_time = hora if isinstance(hora, time) else datetime.strptime(hora, '%H:%M').time()
        
        if hora_time < self.HORA_INICIO or hora_time > self.HORA_CIERRE:
            self.add_error('hora', f"El horario de reserva es de {self.HORA_INICIO.strftime('%H:%M')} a {self.HORA_CIERRE.strftime('%H:%M')}.")
        
        # Validación de minutos (solo :00 o :30)
        if hora_time.minute not in [0, 30]:
            self.add_error('hora', "Las reservas deben ser en punto o media hora (ej: 12:00, 12:30).")
        
        # Validación de solapamiento (solo si no hay errores previos)
        if not self.errors:
            if Reserva.objects.filter(fecha=fecha, hora=hora_time, zona=zona).exists():
                self.add_error('hora', "Esta hora ya está reservada para la zona seleccionada.")

        return cleaned_data