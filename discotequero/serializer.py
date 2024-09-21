from rest_framework import serializers
from .models import Discotequero

class DiscotequeroSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Discotequero' a formatos fácilmente intercambiables (JSON).
    Utiliza el Meta para especificar que se deben incluir todos los campos del modelo.
    """

    class Meta:
        model = Discotequero
        fields = '__all__'
