from django.shortcuts import render
from .models import Etiqueta
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EtiquetaSerializer
from establecimiento.models import Establecimiento
from fiestero.models import Fiestero
from .models import EtiquetaEstablecimiento, EtiquetasFiestero
from .serializer import EtiquetaEstablecimientoSerializer, EtiquetasFiesteroSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.


class EtiquetasView(APIView):
    def get(self, request):
        try:
            etiquetas = Etiqueta.objects.all()
            serializer = EtiquetaSerializer(etiquetas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class EstablecimientoEtiquetasView(APIView):
    def get(self, request, pk):
        """
        Obtiene las etiquetas asociadas a un establecimiento.
        """
        establecimiento = Establecimiento.objects.get(pk=pk)
        etiquetas_establecimiento = EtiquetaEstablecimiento.objects.filter(establecimiento=establecimiento)

        # Serializar las etiquetas
        etiquetas = [etiqueta.etiqueta.nombre for etiqueta in etiquetas_establecimiento]

        return Response({"etiquetas": etiquetas}, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        """
        Crea nuevas etiquetas asociadas a un establecimiento.
        """
        establecimiento = Establecimiento.objects.get(pk=pk)
        etiquetas_ids = request.data.get('etiquetas')  # Esperamos una lista de IDs de etiquetas

        # Verificamos si las etiquetas proporcionadas existen
        etiquetas = Etiqueta.objects.filter(id__in=etiquetas_ids)
        
        # Creamos las relaciones entre las etiquetas y el establecimiento
        for etiqueta in etiquetas:
            if not EtiquetaEstablecimiento.objects.filter(etiqueta=etiqueta, establecimiento=establecimiento).exists():
                EtiquetaEstablecimiento.objects.create(etiqueta=etiqueta, establecimiento=establecimiento)

        return Response({'detail': 'Etiquetas creadas exitosamente.'}, status=status.HTTP_201_CREATED)
    
    def patch(self, request, pk):
        """
        Actualiza las etiquetas asociadas a un establecimiento.
        El discotequero puede deseleccionar etiquetas.
        """
        establecimiento = Establecimiento.objects.get(pk=pk)
        etiquetas_ids = request.data.get('etiquetas')  # Lista de etiquetas seleccionadas

        # Obtener las etiquetas actuales asociadas al establecimiento
        etiquetas_actuales = EtiquetaEstablecimiento.objects.filter(establecimiento=establecimiento)

        # Eliminar las etiquetas no seleccionadas
        etiquetas_a_eliminar = etiquetas_actuales.exclude(etiqueta__id__in=etiquetas_ids)
        etiquetas_a_eliminar.delete()

        # Añadir las nuevas etiquetas
        etiquetas_nuevas = Etiqueta.objects.filter(id__in=etiquetas_ids)
        for etiqueta in etiquetas_nuevas:
            if not EtiquetaEstablecimiento.objects.filter(etiqueta=etiqueta, establecimiento=establecimiento).exists():
                EtiquetaEstablecimiento.objects.create(etiqueta=etiqueta, establecimiento=establecimiento)

        return Response({'detail': 'Etiquetas actualizadas exitosamente.'}, status=status.HTTP_200_OK)



class EtiquetasFiesteroApi(APIView):
    
    def get(self, request, pk_fiestero):
        """
        Obtiene las etiquetas de interés de un fiestero.
        """

        fiestero = get_object_or_404(Fiestero, pk=pk_fiestero)

        # Obtener las etiquetas relacionadas con el fiestero
        etiquetas_fiestero = EtiquetasFiestero.objects.filter(fiestero=fiestero)
        
        # Serializar las etiquetas
        etiquetas = [etiqueta.etiqueta.nombre for etiqueta in etiquetas_fiestero]
        
        return Response({"etiquetas": etiquetas}, status=status.HTTP_200_OK)
    
    
    def post(self, request, pk_fiestero):
        """
        Asigna nuevas etiquetas de interés a un fiestero.
        """
        fiestero = get_object_or_404(Fiestero, pk=pk_fiestero)

        # Obtener los IDs de las etiquetas que se desean asignar
        etiquetas_ids = request.data.get('etiquetas', [])
        
        # Verificar si las etiquetas existen
        etiquetas = Etiqueta.objects.filter(id__in=etiquetas_ids)
        if len(etiquetas) != len(etiquetas_ids):
            return Response({"detail": "Algunas de las etiquetas no existen."}, status=status.HTTP_400_BAD_REQUEST)

        # Asignar las etiquetas al fiestero
        for etiqueta in etiquetas:
            # Crear una nueva relación si no existe
            EtiquetasFiestero.objects.get_or_create(fiestero=fiestero, etiqueta=etiqueta)

        return Response({"detail": "Etiquetas asignadas exitosamente."}, status=status.HTTP_201_CREATED)
    
    
    def patch(self, request, pk_fiestero):
        """
        Actualiza las etiquetas de interés de un fiestero. Elimina las etiquetas antiguas y agrega las nuevas.
        """

        fiestero = get_object_or_404(Fiestero, pk=pk_fiestero)

        # Obtener los nuevos IDs de etiquetas
        etiquetas_ids = request.data.get('etiquetas', [])
        
        # Verificar si las etiquetas existen
        etiquetas = Etiqueta.objects.filter(id__in=etiquetas_ids)
        if len(etiquetas) != len(etiquetas_ids):
            return Response({"detail": "Algunas de las etiquetas no existen."}, status=status.HTTP_400_BAD_REQUEST)

        # Eliminar las relaciones antiguas
        EtiquetasFiestero.objects.filter(fiestero=fiestero).delete()

        # Crear las nuevas relaciones
        for etiqueta in etiquetas:
            EtiquetasFiestero.objects.create(fiestero=fiestero, etiqueta=etiqueta)

        return Response({"detail": "Etiquetas actualizadas exitosamente."}, status=status.HTTP_200_OK)
    