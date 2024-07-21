from django.db import models

# Create your models here.
class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()
    reservar = models.BooleanField(default=False)
    lugar = models.CharField(max_length=100)
    cantidad_reservas = models.IntegerField(default=0)
    # imagen = models.ImageField(upload_to='eventos', null=True, blank=True)

    def __str__(self):
        return self.nombre
