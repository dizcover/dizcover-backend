from rest_framework import serializers
from .models import Users
from discotequero.serializer import DiscotequeroSerializer
from fiestero.serializer import FiesteroSerializer

class UserSerializer(serializers.ModelSerializer):
    # Campos anidados que se agregarán condicionalmente
    fiestero = FiesteroSerializer(read_only=True)
    discotequero = DiscotequeroSerializer(read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'nombre_usuario', 'email', 'nombre_completo', 'foto_perfil', 'tipo', 'fiestero', 'discotequero']

    def to_representation(self, instance):
        """
        Sobrescribir el método `to_representation` para incluir los datos de Fiestero o Discotequero
        según el tipo de usuario.
        """
        representation = super().to_representation(instance)
        
        # Si el tipo de usuario es 'fiestero', incluir los datos del fiestero
        if instance.tipo == 'fiestero':
            representation['fiestero'] = FiesteroSerializer(instance.fiestero).data
            del representation['discotequero']  # Eliminar el campo 'discotequero' si no es relevante
        
        # Si el tipo de usuario es 'discotequero', incluir los datos del discotequero
        elif instance.tipo == 'discotequero':
            representation['discotequero'] = DiscotequeroSerializer(instance.discotequero).data
            del representation['fiestero']  # Eliminar el campo 'fiestero' si no es relevante
        
        return representation