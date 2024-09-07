from rest_framework import serializers
from .models import Favorito, Fiestero

class FavoritotoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Favorito
        fields = '_all_'

class FiesteroSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Fiestero
        fields = '_all_'