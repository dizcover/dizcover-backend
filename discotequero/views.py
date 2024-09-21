
from rest_framework import viewsets
from .serializer import DiscotequeroSerializer
from .models import Discotequero

class DicotequeroViewSet(viewsets.ModelViewSet):
    queryset = Discotequero.objects.all()
    serializer_class = DiscotequeroSerializer