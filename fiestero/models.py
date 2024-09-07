from django.db import models

# Create your models here.
class Favorito(models.Model):
    """
    Creamos la clase Favorito con los campos que queremos que tenga la tabla en la base de datos.
    lo relacionamos con la tabla Establecimiento mediante una clave foránea.

    on_delete=models.CASCADE: indica que si se borra un establecimiento, se borran todos los favoritos que lo tengan.
    related_name='favoritos': indica que desde un establecimiento se puede acceder a todos los favoritos que tiene.


    POR HACER: implementar la relación con el usuario que ha marcado el establecimiento como favorito.
    """
    fiestero = models.ForeignKey("Fiestero", on_delete=models.CASCADE, null=True)
    establecimiento = models.ForeignKey('establecimiento.Establecimiento', on_delete=models.CASCADE, related_name='favoritos')

    def __str__(self):
        """
        Esta función devuelve una representación en cadena de un objeto Favorito. en el cual se muestra cual es el establecimiento favorito.
        """

        return f'{self.fiestero.nombre_usuario} - {self.establecimiento.nombre}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fiestero', 'establecimiento'], name='unique_fiestero_establecimiento')
        ]



class Fiestero(models.Model):
    """
    Creamos la clase Fiestero con los campos que queremos que tenga la tabla en la base de datos.
    """
    
    correo = models.EmailField()
    nombre_usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)
    
    foto_perfil = models.CharField(max_length=100)

    nombre_completo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateField()

    # Seria mejor solo un campo para el numero de identificacion y otro para el tipo??
    num_identificación = models.CharField(max_length=100)
    pasaporte = models.CharField(max_length=100)

    # indentidad_sexo = models.CharField(max_length=100)
    # id_etiquetas

    def __str__(self):
        return self.nombre_usuario