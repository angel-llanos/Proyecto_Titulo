from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROL_CHOICES = (
        (1, 'Cliente'),
        (2, 'Mesero'),
        (3, 'Cocinero'),
        (4, 'Administrador'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROL_CHOICES, default=1)

    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = 4  #4 = rol admin
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    