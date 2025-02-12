from rest_framework import serializers
from .models import Evento, ImagenEvento, Asiento

class EventoSerializer(serializers.ModelSerializer):
    """
    Este serializador convierte el modelo 'Evento' a JSON.
    """
    primera_imagen = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = '__all__'

    def get_primera_imagen(self, obj):
        """
        Obtiene la primera imagen asociada al evento.
        """
        primera_imagen = obj.imagenes.first()  # Relación inversa usando 'imagenes'
        if primera_imagen:
            return primera_imagen.imagen.url  # Retorna la URL de la imagen
        return None

class ImagenEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenEvento
        fields = '__all__'


class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiento
        fields = '__all__'