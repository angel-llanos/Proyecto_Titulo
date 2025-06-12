from django.db import models
from django.conf import settings
from apps.menus.models import Menu 

class Zona(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)  #mesa disponible o no

    def __str__(self):
        return f"Mesa {self.numero} - Zona {self.zona.nombre}"

class Reserva(models.Model):
    ESTADOS_RESERVA = (
        ('borrador', 'Borrador'),
        ('completada', 'Completada'),
    )

    id_reserva = models.CharField(max_length=12, unique=True, editable=False)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre_reserva = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    telefono = models.CharField(max_length=20)
    comensales = models.PositiveIntegerField(default=1)
    abono = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    mesas = models.ManyToManyField('Mesa')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)  #modelo menú
    zona = models.ForeignKey('Zona', on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='borrador')

    def save(self, *args, **kwargs):
        if not self.id_reserva:
            super().save(*args, **kwargs)
            self.id_reserva = self.generar_id_alfanumerico()
            super().save(update_fields=['id_reserva'])
        else:
            super().save(*args, **kwargs)

    def generar_id_alfanumerico(self):
        import string
        base36 = ''
        chars = string.digits + string.ascii_uppercase
        num = self.id
        while num > 0:
            num, i = divmod(num, 36)
            base36 = chars[i] + base36
        return base36.zfill(6)

    def __str__(self):
        return f"Reserva de {self.cliente.username} para {self.fecha} {self.hora}"