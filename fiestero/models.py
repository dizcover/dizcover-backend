from django.db import models
from autenticacion.models import Users
from enum import Enum
from establecimiento.models import Establecimiento

class Favorito(models.Model):
    """
    La clase Favorito representa la relación entre un fiestero (usuario) y un establecimiento marcado como favorito.

    Campos:
        - fiestero (ForeignKey): Referencia al usuario que marca el establecimiento como favorito.
        - establecimiento (ForeignKey): Referencia al establecimiento que es marcado como favorito.
    
    Relaciones:
        - La relación con Establecimiento se define mediante una clave foránea, con el comportamiento on_delete=models.CASCADE
          para eliminar automáticamente los favoritos si se elimina el establecimiento.
        - related_name='favoritos': Permite que un establecimiento tenga acceso a los favoritos que lo incluyen.
    
    Restricciones:
        - Se establece una restricción de unicidad entre 'fiestero' y 'establecimiento' para evitar duplicados,
          de forma que un fiestero no pueda marcar un mismo establecimiento como favorito más de una vez.
    """

    fiestero = models.ForeignKey("Fiestero", on_delete=models.CASCADE, null=True)
    establecimiento = models.ForeignKey('establecimiento.Establecimiento', on_delete=models.CASCADE, related_name='favoritos')

    def __str__(self):
        """
        Método especial que define la representación en cadena de un objeto Favorito.

        Devuelve una cadena en el formato 'nombre_usuario - nombre_establecimiento', útil para identificación
        rápida del favorito.
        """
        return f'{self.fiestero.user.nombre_usuario} - {self.establecimiento.nombre}'

    class Meta:
        """
        Meta clase que contiene configuraciones adicionales para el modelo Favorito. Estas restricciones se ven más que nada desde el panel del administrador

        Restricciones:
            - UniqueConstraint: Establece que la combinación de 'fiestero' y 'establecimiento' debe ser única.
              Esta restricción garantiza que un mismo usuario no pueda marcar el mismo establecimiento como favorito más de una vez.
        """
        constraints = [
            models.UniqueConstraint(fields=['fiestero', 'establecimiento'], name='unique_fiestero_establecimiento')
        ]




class Fiestero(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='fiestero')
    # Campos específicos de Fiestero
    identidad_sexo = models.CharField(max_length=20, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No binario'),
        ('O', 'Otro'),
        ('PND', 'Prefiero no decirlo')
    ])
    num_identificacion = models.CharField(max_length=20)
    pasaporte = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.user.nombre_usuario



class CalificacionEnum(Enum):
    UNO = 1, "1 Estrella"
    DOS = 2, "2 Estrellas"
    TRES = 3, "3 Estrellas"
    CUATRO = 4, "4 Estrellas"
    CINCO = 5, "5 Estrellas"

class FeedBack(models.Model):
    fiestero = models.ForeignKey(Fiestero, on_delete=models.CASCADE)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    comentario = models.TextField(null=True, blank=True, max_length=500)
    calificacion = models.IntegerField(choices=[(tag.value[0], tag.value[1]) for tag in CalificacionEnum], default=CalificacionEnum.UNO.value[0])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calificación de {self.fiestero} para el establecimiento {self.establecimiento}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fiestero', 'establecimiento'], name='unique_fiestero_establecimiento_feedback')
        ]
