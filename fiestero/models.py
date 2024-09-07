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

    establecimiento = models.ForeignKey('establecimiento.Establecimiento', on_delete=models.CASCADE, related_name='favoritos')

    def __str__(self):
        """
        Esta función devuelve una representación en cadena de un objeto Favorito. en el cual se muestra cuañ es el establecimiento favorito.
        """

        return f'Favorito - {self.establecimiento.nombre}'