from django.db import models
from establecimiento.models import Establecimiento
from django.utils.text import slugify
# Create your models here.

def upload_to_establecimiento(instance, filename):
    """
    Genera una ruta dinámica para almacenar las imágenes en base al nombre del establecimiento.
    """
    nombre_evento = slugify(instance.evento.nombre) if instance.evento and instance.evento.nombre else "sin_nombre"
    return f'establecimientos/images/{nombre_evento}/eventos/{filename}'

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()
    reservar = models.BooleanField(default=False)
    lugar = models.CharField(max_length=100)
    cantidad_reservas = models.IntegerField(default=0)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, null=True, blank=True)

    

    def __str__(self):
        return self.nombre

class ImagenEvento(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to=upload_to_establecimiento, null=True)

    def __str__(self):
        return f"Imagen de {self.evento.nombre}"