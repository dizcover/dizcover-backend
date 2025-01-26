from django.db import models
from establecimiento.models import Establecimiento
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
import os
import boto3
from dotenv import load_dotenv
# Create your models here.

def upload_to_establecimiento(instance, filename):
    """
    Genera una ruta dinámica para almacenar las imágenes en base al nombre del establecimiento y del evento.
    """
    nombre_establecimiento = slugify(instance.evento.establecimiento.nombre) if instance.evento and instance.evento.establecimiento and instance.evento.establecimiento.nombre else "sin_nombre_establecimiento"
    nombre_evento = slugify(instance.evento.nombre) if instance.evento and instance.evento.nombre else "sin_nombre_evento"
    return f'establecimientos/images/{nombre_establecimiento}/eventos/{nombre_evento}/{filename}'

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
    
    def save(self, *args, **kwargs):
        if self.imagen:
            # Convertir la imagen a WebP y subirla con el Content-Type correcto
            self.imagen = self.convert_to_webp(self.imagen)

        super().save(*args, **kwargs)

    def convert_to_webp(self, image_field):
        """
        Convierte la imagen a formato WebP y sube a S3 con el Content-Type 'image/webp'.
        """
        # Abre la imagen original
        image = Image.open(image_field)

        # Convierte a formato RGB (necesario para WebP)
        image = image.convert("RGB")

        # Genera un archivo WebP en memoria
        buffer = BytesIO()
        image.save(buffer, format="WEBP")
        buffer.seek(0)

        # Configura S3
        load_dotenv()
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

        # Genera la ruta dinámica usando el método 'upload_to_establecimiento'
        filename = os.path.basename(image_field.name)
        webp_key = upload_to_establecimiento(self, f"{os.path.splitext(filename)[0]}.webp")

        # Subir el archivo con el tipo MIME correcto
        s3_client.put_object(
            Bucket=bucket_name,
            Key=webp_key,
            Body=buffer,
            ContentType='image/webp'
        )

        # Retornar la URL del archivo en S3
        return webp_key
