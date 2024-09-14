from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
from .models import Favorito, Fiestero
from establecimiento.models import Establecimiento
from .serializer import FavoritotoSerializer
from django.shortcuts import get_object_or_404

class FavoritoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar la creación y visualización de favoritos.
    """
    queryset = Favorito.objects.all()
    serializer_class = FavoritotoSerializer

    @transaction.atomic #Con este decorador hacemos garantiazar que si falla algo en el proceso, no se vera en la base de datos información incompleta dado a esto.
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo favorito solo si no existe uno previamente para el mismo fiestero y establecimiento.
        """

        # Obtenemos los id de cada entidad relacionada
        fiestero_id = request.data.get('fiestero')
        establecimiento_id = request.data.get('establecimiento')

        # En dado caso de que no haya algun id o no exista, se debe mandar error
        if not fiestero_id or not establecimiento_id:
            return Response(
                {'detail': 'Debe proporcionar fiestero y establecimiento.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Verificar si los objetos existen
            fiestero = get_object_or_404(Fiestero, id=fiestero_id)
            establecimiento = get_object_or_404(Establecimiento, id=establecimiento_id)
        except:
            return Response(
                {'detail': 'Fiestero o establecimiento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Se maneja desde esta vista el tema de no crear una relacion fiestero y esablecimeinto en favoritos existente
        if Favorito.objects.filter(fiestero_id=fiestero_id, establecimiento_id=establecimiento_id).exists():
            return Response(
                {'detail': 'Este establecimiento ya está marcado como favorito por este usuario.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si no pasa nada, creamos la entidad
        return super().create(request, *args, **kwargs)
