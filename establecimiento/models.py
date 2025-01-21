from django.db import models
from django.utils.text import slugify
from enum import Enum
from PIL import Image
from io import BytesIO
import os
import boto3
from dotenv import load_dotenv

class Establecimiento(models.Model):
    """
    La clase Establecimiento representa un lugar de entretenimiento, como una discoteca o bar.

    Campos:
        - id_discotequero (ForeignKey): Referencia al discotequero que administra el establecimiento.
        - nombre (CharField): Nombre del establecimiento.
        - direccion (CharField): Dirección física del establecimiento.
        - telefono (CharField): Número de teléfono de contacto del establecimiento.
        - email (EmailField): Correo electrónico de contacto del establecimiento.
        - descripcion (TextField): Descripción detallada del establecimiento.
        - ciudad (CharField): Ciudad donde se encuentra el establecimiento.
        - municipio (CharField): Municipio donde se encuentra el establecimiento.
        - id_coordenada (ForeignKey): Referencia a las coordenadas geográficas del establecimiento.
        - id_horario (ForeignKey): Referencia al horario de funcionamiento del establecimiento.
    
    Relaciones:
        - La relación con Discotequero se define mediante una clave foránea, con el comportamiento on_delete=models.CASCADE
          para eliminar automáticamente el establecimiento si se elimina el discotequero.
        - La relación con Coordenada y Horario se define mediante claves foráneas.
        - related_name='establecimientos': Permite que un discotequero tenga acceso a los establecimientos que administra.
    
    Restricciones:
    - UniqueConstraint: Establece que la combinación de 'nombre' y 'direccion' debe ser única.
        Esta restricción garantiza que no puede haber dos establecimientos con el mismo nombre y dirección.

    - UniqueConstraint: Establece que la combinación de 'nombre' y 'discotequero_id' debe ser única.
        Esta restricción garantiza que un discotequero no puede tener dos establecimientos con el mismo nombre.
    """

    id_discotequero = models.ForeignKey('discotequero.Discotequero', on_delete=models.CASCADE, null=True, related_name='establecimientos')
    nombre = models.CharField(max_length=100, null=True)
    direccion = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    descripcion = models.TextField(null=True)

    departamento = models.CharField(max_length=100, null=True)
    municipio = models.CharField(max_length=100, null=True)
    # id_coordenada = models.ForeignKey('Coordenada', on_delete=models.CASCADE, null=True)
    # id_horario = models.ForeignKey('Horario', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        constraints = [
            # No puede haber dos establecimientos con el mismo nombre y dirección (Se debe mejorar esta validacion)
            models.UniqueConstraint(fields=['nombre', 'direccion', 'departamento', 'municipio'], name='unique_nombre_direccion_departamento_municipio'),
            models.UniqueConstraint(fields=['nombre', 'id_discotequero'], name='unique_nombre_discotequero') # No puede haber dos establecimientos con el mismo nombre y discotequero (Evitar que un discotequero tenga dos establecimientos con el mismo nombre)
        ]


def upload_to_establecimiento(instance, filename):
    """
    Genera una ruta dinámica para almacenar las imágenes en base al nombre del establecimiento.
    """
    nombre_establecimiento = slugify(instance.establecimiento.nombre) if instance.establecimiento and instance.establecimiento.nombre else "sin_nombre"
    return f'establecimientos/images/{nombre_establecimiento}/{filename}'


class ImagenEstablecimiento(models.Model):
    establecimiento = models.ForeignKey('Establecimiento', on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.FileField(upload_to=upload_to_establecimiento, null=True)

    def __str__(self):
        if self.establecimiento and self.establecimiento.nombre:
            return f"Imagen del establecimiento: {self.establecimiento.nombre}"
        return "Imagen sin nombre"

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


class Coordenada(models.Model):
    establecimiento = models.OneToOneField('Establecimiento', on_delete=models.CASCADE, related_name='coordenada', null=True, blank=True)
    latitud = models.FloatField()  # Latitud del punto geográfico
    longitud = models.FloatField()  # Longitud del punto geográfico
    # Puedes agregar un campo adicional si deseas almacenar información sobre el hemisferio
    hemisferio_lat = models.CharField(max_length=1, choices=[('N', 'Norte'), ('S', 'Sur')], null=True, blank=True)
    hemisferio_lon = models.CharField(max_length=1, choices=[('E', 'Este'), ('O', 'Oeste')], null=True, blank=True)

    def __str__(self):
        return f"Lat: {self.latitud}, Lon: {self.longitud}"


class DiaSemanaEnum(Enum):
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"
    DOMINGO = "Domingo"
    
class Horario(models.Model):
    dia = models.CharField(
        max_length=20,
        choices=[(dia.name, dia.value) for dia in DiaSemanaEnum],
        default=DiaSemanaEnum.LUNES.name
    )
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()

    def __str__(self):
        return f"{self.dia} - {self.hora_apertura} - {self.hora_cierre}"


class HorarioEstablecimiento(models.Model):
    establecimiento = models.ForeignKey('Establecimiento', on_delete=models.CASCADE, related_name='horarios')
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE)

    def __str__(self):
        return f"Horario de {self.establecimiento.nombre} para el {self.horario.dia}. Aperura: {self.horario.hora_apertura} - Cierre: {self.horario.hora_cierre}"
