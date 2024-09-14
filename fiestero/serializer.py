from rest_framework import serializers
from .models import Favorito, Fiestero

class FavoritotoSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Favorito' a formatos fácilmente intercambiables (JSON).
    Utiliza el Meta para especificar que se deben incluir todos los campos del modelo.
    """
    class Meta:
        model = Favorito
        fields = '__all__'  # Incluir todos los campos del modelo Favorito


class FiesteroSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo 'Fiestero'.
    También incluye todos los campos del modelo de usuario Fiestero.
    """
    class Meta:
        model = Fiestero
        fields = '__all__'  # Incluir todos los campos del modelo Fiestero
