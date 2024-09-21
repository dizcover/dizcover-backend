from django.db import models

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
        - imagen (CharField): URL o ruta de la imagen representativa del establecimiento (puede ser nulo).
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
    imagen = models.CharField(max_length=100, null=True)
    departamento = models.CharField(max_length=100, null=True)
    municipio = models.CharField(max_length=100, null=True)
    id_coordenada = models.ForeignKey('Coordenada', on_delete=models.CASCADE, null=True)
    id_horario = models.ForeignKey('Horario', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        constraints = [
            # No puede haber dos establecimientos con el mismo nombre y dirección (Se debe mejorar esta validacion)
            models.UniqueConstraint(fields=['nombre', 'direccion', 'departamento', 'municipio'], name='unique_nombre_direccion_departamento_municipio'),
            models.UniqueConstraint(fields=['nombre', 'id_discotequero'], name='unique_nombre_discotequero') # No puede haber dos establecimientos con el mismo nombre y discotequero (Evitar que un discotequero tenga dos establecimientos con el mismo nombre)
        ]

class Coordenada(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    direccion = models.CharField(max_length=100)
    este = models.CharField(max_length=100)
    oeste = models.CharField(max_length=100)

    def __str__(self):
        return self.direccion
    
class Horario(models.Model):
    dias = models.CharField(max_length=100)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()

    def __str__(self):
        return f"{self.dias} - {self.hora_apertura} - {self.hora_cierre}"