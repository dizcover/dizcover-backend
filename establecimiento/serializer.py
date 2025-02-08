from rest_framework import serializers
from .models import Establecimiento, Coordenada, Horario, ImagenEstablecimiento, HorarioEstablecimiento, Coordenada
from recomendacion.models import EtiquetaEstablecimiento

class EstablecimientoSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Establecimiento' a JSON.
    """
    primera_imagen = serializers.SerializerMethodField()
    etiquetas = serializers.SerializerMethodField()  

    class Meta:
        model = Establecimiento
        fields = '__all__'

    def get_primera_imagen(self, obj):
        # Obtener la primera imagen asociada al establecimiento
        primera_imagen = obj.imagenes.first()  # Relación inversa usando 'imagenes'
        if primera_imagen:
            return primera_imagen.imagen.url  # Asegúrate de que la imagen tenga la URL
        return None
    
    def get_etiquetas(self, obj):
        """
        Devuelve los nombres de las etiquetas asociadas al establecimiento.
        """
        etiquetas = EtiquetaEstablecimiento.objects.filter(establecimiento=obj)
        if etiquetas:
            # Aquí devolvemos los nombres de las etiquetas, no sus IDs
            return [etiqueta.etiqueta.nombre for etiqueta in etiquetas]
        return []  # Retorna una lista vacía si no tiene etiquetas



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

class CoordenadaSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Coordenada' a JSON.
    """
    class Meta:
        model = Coordenada
        fields = '__all__'