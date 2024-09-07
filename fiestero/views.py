from django.shortcuts import render
from rest_framework import viewsets
from .serializer import FavoritotoSerializer
from .models import Favorito, Fiestero
from rest_framework.response import Response

# Create your views here.


class FavoritoViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritotoSerializer

    # def create(self, request, *args, **kwargs):
    #     print(request)
    #     usuario = request.user.fiestero
    #     establecimiento = request.data.get('establecimiento')

    #     if Favorito.objects.filter(fiestero=usuario, establecimiento=establecimiento).exists():
    #         return Response({'error': 'Ya existe el favorito'}, status=400)
        
    #     return super().create(request, *args, **kwargs)