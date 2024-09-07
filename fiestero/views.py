from django.shortcuts import render
from rest_framework import viewsets
from .serializer import FavoritotoSerializer
from .models import Favorito
# Create your views here.


class FavoritoViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritotoSerializer