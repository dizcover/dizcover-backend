from django.db import models
from autenticacion.models import Users

# Create your models here.
class Discotequero(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='discotequero')
    # Campos específicos de Discotequero
    nombre_empresarial = models.CharField(max_length=100)
    NIT = models.CharField(max_length=20)
    NIT_verificado = models.BooleanField(default=False)
    digito_verificacion = models.CharField(max_length=32) # Debemos generar un uuid para este campo, por eso los 32 caracteres.