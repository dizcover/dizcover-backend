from rest_framework import viewsets
from .serializer import DiscotequeroSerializer
from .models import Discotequero

from rest_framework.decorators import action
from rest_framework.response import Response
from establecimiento.models import Establecimiento
from establecimiento.serializer import EstablecimientoSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound

class DicotequeroViewSet(viewsets.ModelViewSet):
    queryset = Discotequero.objects.all()
    serializer_class = DiscotequeroSerializer

    @action(detail=True, methods=['get'])
    def establecimientos(self, request, pk=None):
        try:
            discotequero = self.get_object()
        except Discotequero.DoesNotExist:
            raise NotFound(detail="Discotequero no encontrado", code=status.HTTP_404_NOT_FOUND)

        # Pendiente: Verificar si el usuario autenticado es el propietario del discotequero
        
        establecimientos = Establecimiento.objects.filter(id_discotequero=discotequero)
        serializer = EstablecimientoSerializer(establecimientos, many=True)
        return Response(serializer.data)