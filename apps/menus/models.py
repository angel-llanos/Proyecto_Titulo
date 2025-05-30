from django.db import models

# Create your models here.
class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes_menus/', blank=True, null=True)

    def __str__(self):
        return self.nombre