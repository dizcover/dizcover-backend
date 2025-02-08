from django.db import models
from establecimiento.models import Establecimiento
from fiestero.models import Fiestero

class Etiqueta(models.Model):
    GENERO = 'G'
    AMBIENTE = 'A'
    ESPECIAL = 'E'

    TIPO_ETIQUETA_CHOICES = [
        (GENERO, 'Genero'),
        (AMBIENTE, 'Ambiente'),
        (ESPECIAL, 'Especial'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la etiqueta
    tipo = models.CharField(
        max_length=1,
        choices=TIPO_ETIQUETA_CHOICES,
        default=GENERO
    )

    def __str__(self):
        return self.nombre
    
class EtiquetaEstablecimiento(models.Model):
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE, related_name='etiquetas')
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.etiqueta} - {self.establecimiento}'
    
    class Meta:
        unique_together = ('etiqueta', 'establecimiento')

class EtiquetasFiestero(models.Model):
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    fiestero = models.ForeignKey(Fiestero, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.etiqueta} - {self.fiestero}'
    
    class Meta:
        unique_together = ('etiqueta', 'fiestero')

    

