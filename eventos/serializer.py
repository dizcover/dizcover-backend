from rest_framework import serializers
from .models import Evento, ImagenEvento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'


class ImagenEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenEvento
        fields = '__all__'