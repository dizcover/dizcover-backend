from .models import Etiqueta, EtiquetaEstablecimiento, EtiquetasFiestero
from rest_framework import serializers

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class EtiquetaEstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtiquetaEstablecimiento
        fields = '__all__'

class EtiquetasFiesteroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtiquetasFiestero
        fields = '__all__'