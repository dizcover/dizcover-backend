from django.db import models

# Create your models here
class Establecimiento(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.EmailField()
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre