from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
from .models import Favorito, Fiestero
from establecimiento.models import Establecimiento
from .serializer import FavoritotoSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class FavoritoViewSet(APIView):
    """
    Vista para gestionar los favoritos de un fiestero.
    """

    def get_fiestero(self, fiestero_id):
        """Obtiene el fiestero a partir del id"""
        return get_object_or_404(Fiestero, id=fiestero_id)

    def get_establecimiento(self, establecimiento_id):
        """Obtiene el establecimiento a partir del id"""
        return get_object_or_404(Establecimiento, id=establecimiento_id)

    def post(self, request, fiestero_id):
        """
        Crea un nuevo favorito solo si no existe uno previamente para el mismo fiestero y establecimiento.
        """
        establecimiento_id = request.data.get('establecimiento')

        if not establecimiento_id:
            return Response(
                {'detail': 'Debe proporcionar el id del establecimiento.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener fiestero
        fiestero = self.get_fiestero(fiestero_id)

        # Obtener establecimiento
        establecimiento = self.get_establecimiento(establecimiento_id)

        # Verificar si ya existe este favorito
        if Favorito.objects.filter(fiestero=fiestero, establecimiento=establecimiento).exists():
            return Response(
                {'detail': 'Este establecimiento ya está marcado como favorito por este usuario.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el favorito
        favorito = Favorito.objects.create(fiestero=fiestero, establecimiento=establecimiento)

        # Serializar el favorito creado
        serializer = FavoritotoSerializer(favorito)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, fiestero_id):
        """
        Lista los favoritos de un fiestero basado en su id que se pasa en la URL.
        """
        fiestero = self.get_fiestero(fiestero_id)

        # Obtener favoritos de este fiestero
        favoritos = Favorito.objects.filter(fiestero=fiestero)

        # Serializar los favoritos
        serializer = FavoritotoSerializer(favoritos, many=True)
        return Response(serializer.data)

    def delete(self, request, fiestero_id):
        """
        Elimina un favorito basado en el id del fiestero y el id del establecimiento.
        """
        establecimiento_id = request.data.get('establecimiento')

        if not establecimiento_id:
            return Response(
                {'detail': 'Debe proporcionar el id del establecimiento.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener fiestero
        fiestero = self.get_fiestero(fiestero_id)

        # Obtener establecimiento
        establecimiento = self.get_establecimiento(establecimiento_id)

        # Buscar el favorito
        favorito = get_object_or_404(Favorito, fiestero=fiestero, establecimiento=establecimiento)

        # Eliminar el favorito
        favorito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)