from rest_framework import serializers
from .models import Establecimiento, Coordenada, Horario, ImagenEstablecimiento

class EstablecimientoSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Establecimiento' a JSON.
    """
    class Meta:
        model = Establecimiento
        fields = '__all__'

class ImagenEstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenEstablecimiento
        fields = ['id', 'establecimiento', 'imagen']  

class CoordenadaSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Coordenada' a JSON.
    """
    class Meta:
        model = Coordenada
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Horario' a JSON.
    """
    class Meta:
        model = Horario
        fields = '__all__'