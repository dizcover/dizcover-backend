from django.db import models

# Create your models here.

class EnumGenero(models.TextChoices):
    REGGAETON = 'Reggaeton'
    POP = 'Pop'
    ROCK = 'Rock'
    ELECTRONICA = 'Electronica'
    HIPHOP = 'HipHop'
    SALSA = 'Salsa'
    MERENGUE = 'Merengue'
    BACHATA = 'Bachata'
    VALLENATO = 'Vallenato'

    # Colocar más géneros musicales


class EnumAmbiente(models.TextChoices):
    DISCO = 'Disco'
    BAR = 'Bar'
    KARAOKE = 'Karaoke'
    TOMAR = 'Tomar'

    # Colocar más ambientes

class EnumEspeciales(models.TextChoices):
    SWINGER = 'Swinger'
    LGBTIQ = 'LGBTIQ+'

class Genero(models.Model):
    etiqueta_genero = models.CharField(max_length=150, choices=EnumGenero.choices)
    def __str__(self):
        return self.etiqueta_genero
    

class Ambiente(models.Model):
    etiqueta_ambiente = models.CharField(max_length=150)

    def __str__(self):
        return self.etiqueta_ambiente

class ESpeciales(models.Model):
    etiqueta_especiales = models.CharField(max_length=150)

    def __str__(self):
        return self.etiqueta_especiales
    

class Etiquetas(models.Model):
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, null=True)
    especiales = models.ForeignKey(ESpeciales, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.genero} - {self.ambiente} - {self.especiales}'

    
