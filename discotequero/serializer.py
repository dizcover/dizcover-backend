from rest_framework import serializers
from .models import Discotequero

class DiscotequeroSerializer(serializers.ModelSerializer):


    class Meta:
        model = Discotequero
        fields = '__all__'
