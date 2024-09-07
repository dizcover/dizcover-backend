from rest_framework import serializers
from .models import Favorito

class FavoritotoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Favorito
        fields = '__all__'