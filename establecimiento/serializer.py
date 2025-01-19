from rest_framework import serializers
from .models import Establecimiento, Coordenada, Horario, ImagenEstablecimiento, HorarioEstablecimiento

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

class HorarioEstablecimientoSerializer(serializers.ModelSerializer):
    # Incluyendo el campo 'id' del horario y 'dia' asociado a ese horario
    dia_id = serializers.IntegerField(source='horario.id', read_only=True)
    dia = serializers.CharField(source='horario.dia', read_only=True)
    hora_apertura = serializers.TimeField(source='horario.hora_apertura', read_only=True)
    hora_cierre = serializers.TimeField(source='horario.hora_cierre', read_only=True)

    class Meta:
        model = HorarioEstablecimiento
        fields = ['dia_id', 'dia', 'hora_apertura', 'hora_cierre']  # Incluir id del horario, día y id de la relación