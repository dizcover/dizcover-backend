from rest_framework import viewsets, status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Establecimiento
from discotequero.models import Discotequero
from establecimiento.models import Establecimiento, ImagenEstablecimiento
from rest_framework.views import APIView
from .serializer import EstablecimientoSerializer, ImagenEstablecimientoSerializer




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

        # Obtenemos los datos para validar si ya existe un establecimiento con los mismos datos (Con estos atributos que son esecniales para la creación de un establecimiento)
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
    

# API de imagenes de establecimientos
class ImagenesEstablecimientoView(APIView):
    # Recibe el id del establecimiento al que se le asociará la imagen
    def post(self, request, pk):
        """
        Crea una nueva imagen asociada a un establecimiento.
        """
        try:
            establecimiento = get_object_or_404(Establecimiento, id=pk)
            imagenes_existentes = ImagenEstablecimiento.objects.filter(establecimiento=establecimiento).count()
            imagenes = [request.data.get(f'imagen{i}') for i in range(1, len(request.data)+1)]
            suma_imgenes_guardas_subidas = imagenes_existentes + len([imagen for imagen in imagenes if imagen])

            # Validar el tipo de archivo de las imágenes
            formatos_permitidos = ['image/jpeg', 'image/png', 'image/jpg']
            for imagen in imagenes:
                if imagen and imagen.content_type not in formatos_permitidos:
                    return Response(
                        {'detail': 'Formato de imagen no permitido. Solo se permiten imágenes JPEG, PNG o JPG.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if imagenes_existentes >= 5 or suma_imgenes_guardas_subidas > 5:
                return Response(
                    {'detail': 'El establecimiento no puede tener más de 5 imágenes.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not any(imagenes):
                return Response(
                    {'detail': 'Debe proporcionar al menos una imagen.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_size_mb = sum(imagen.size for imagen in imagenes if imagen) / (1024 * 1024)
            print(total_size_mb)
            if total_size_mb > 5:  # Limite de tamaño total de imágenes en MB
                return Response(
                    {'detail': 'El tamaño total de las imágenes no puede exceder los 5 MB.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for imagen in imagenes:
                if imagen:
                    ImagenEstablecimiento.objects.create(establecimiento=establecimiento, imagen=imagen)
                
            return Response(
                {'detail': 'Imagen/es creada exitosamente.'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def get(self, request, pk):
        """
        Obtiene las imágenes asociadas a un establecimiento.
        """
        try:
            establecimiento = get_object_or_404(Establecimiento, id=pk)
            imagenes = ImagenEstablecimiento.objects.filter(establecimiento=establecimiento)
            serializer = ImagenEstablecimientoSerializer(imagenes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk_imagen):
        """
        Elimina una imagen asociada a un establecimiento.
        """
        try:
            imagen = get_object_or_404(ImagenEstablecimiento, id=pk_imagen)
            imagen.delete()
            return Response(
                {'detail': 'Imagen eliminada exitosamente.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )