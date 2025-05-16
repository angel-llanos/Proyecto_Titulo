import string
from django.db import models
from django.conf import settings

class Zona(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)  # Disponible o no

    def __str__(self):
        return f"Mesa {self.numero} - Zona {self.zona.nombre}"

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

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
    abono = models.DecimalField(max_digits=8, decimal_places=2)
    mesas = models.ManyToManyField('Mesa')
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, blank=True)
    zona = models.ForeignKey('Zona', on_delete=models.CASCADE, null=True, blank=True)
    
    # ➕ NUEVO CAMPO
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='borrador')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.id_reserva:
            self.id_reserva = self.generar_id_alfanumerico()
            super().save(update_fields=['id_reserva'])

    def generar_id_alfanumerico(self):
        base36 = ''
        chars = string.digits + string.ascii_uppercase
        num = self.id
        while num > 0:
            num, i = divmod(num, 36)
            base36 = chars[i] + base36
        return base36.zfill(6)

    def __str__(self):
        return f"Reserva de {self.cliente.username} para {self.fecha} {self.hora}"