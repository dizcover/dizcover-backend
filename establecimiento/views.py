from rest_framework import viewsets, status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Establecimiento
from discotequero.models import Discotequero
from establecimiento.models import Establecimiento

from .serializer import EstablecimientoSerializer

class EstablecimientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar la creación y visualización de Establecimientos.
    """
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer

    @transaction.atomic #Con este decorador hacemos garantiazar que si falla algo en el proceso, no se vera en la base de datos información incompleta dado a esto.
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo establecimiento solo si no existe uno previamente duplicado.
        - La condicion para que un establecimiento sea duplicado es que tenga el mismo nombre y direccion en la misma ciudad. (Se debe mejorar la validacion)
        """

        # Obtenemos los datos para validar si ya existe un establecimiento con los mismos datos
        id_discotequero = request.data.get("id_discotequero")
        nombre = request.data.get("nombre")
        direccion = request.data.get("direccion")
        departamento = request.data.get("departamento")
        municipio = request.data.get("municipio")

        datosIncompletos = not id_discotequero or not nombre or not direccion or not departamento or not municipio
        if datosIncompletos:
            return Response(
                {'detail': 'Debe proporcionar los datos completos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar si el discotequero existe
            get_object_or_404(Discotequero, id=id_discotequero)
        except:
            return Response(
                {'detail': 'Discotequero no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # (Se debe mejorar la validacion)
        # Se maneja desde esta vista el tema de no duplicar un establecimiento
        existeEstablecimiento = Establecimiento.objects.filter(nombre=nombre, direccion=direccion, departamento=departamento, municipio=municipio).exists()
        if existeEstablecimiento:
            return Response(
                {'detail': 'Este establecimiento ya se encuentra registrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # (Se debe mejorar la validacion)
        duplicadoPorDiscotequero = Establecimiento.objects.filter(nombre=nombre, id_discotequero=id_discotequero).exists()
        if duplicadoPorDiscotequero:
            return Response(
                {'detail': 'El discotequero ya tiene un establecimiento con este nombre.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si hay ningun error, crear la entidad
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Actualiza un establecimiento existente solo si cumple con las validaciones.
        """
        id_establecimiento = kwargs.get('pk')
        id_discotequero = request.data.get("id_discotequero")
        nombre = request.data.get("nombre")
        direccion = request.data.get("direccion")
        departamento = request.data.get("departamento")
        municipio = request.data.get("municipio")

        datosIncompletos = not id_establecimiento or not id_discotequero or not nombre or not direccion or not departamento or not municipio
        if datosIncompletos:
            return Response(
                {'detail': 'Debe proporcionar los datos completos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar si el establecimiento existe
            establecimiento = get_object_or_404(Establecimiento, id=id_establecimiento)
        except:
            return Response(
                {'detail': 'Establecimiento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Verificar si el discotequero existe
            get_object_or_404(Discotequero, id=id_discotequero)
        except:
            return Response(
                {'detail': 'Discotequero no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # (Se debe mejorar la validacion)

        # Verificar si el discotequero ya tiene un establecimiento con este nombre
        duplicadoPorDiscotequero = Establecimiento.objects.filter(nombre=nombre, id_discotequero=id_discotequero).exclude(id=id_establecimiento).exists()
        
        if duplicadoPorDiscotequero:
            return Response(
                {'detail': 'El discotequero ya tiene un establecimiento con este nombre.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si no pasa nada, actualizamos la entidad
        return super().update(request, *args, **kwargs)