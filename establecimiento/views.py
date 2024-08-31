from rest_framework import viewsets
from .serializer import EstablecimientoSerializer
from .models import Establecimiento




# Create your views here.
class EstablecimientoViewSet(viewsets.ModelViewSet):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer



