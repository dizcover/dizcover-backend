from rest_framework import viewsets, status
from .serializer import EventoSerializer, ImagenEventoSerializer
from .models import Evento, ImagenEvento
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

# Esto es bascimane la API de eventos, ya su toca cambiar el comportamiento o algo por el estilo, toca modificar y crear las funciones de la API
class EventoViewSet(viewsets.ModelViewSet):
    """
    Una vista basada en conjuntos de vistas (ViewSet) para el modelo Evento.

    Esta clase proporciona las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) 
    para el modelo Evento utilizando un conjunto de vistas de Django REST Framework.

    Atributos:
        queryset (QuerySet): Un conjunto de consultas que contiene todos los objetos del modelo Evento.
        serializer_class (class): La clase de serializador utilizada para convertir instancias de Evento 
                                  a y desde representaciones JSON.
    """

    # Con esto se puede restringir el acceso a la API, solo los usuarios autenticados pueden acceder, por atnto tiene que pasar el token de autenticacion
    # permission_classes = (IsAuthenticated,)
    
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer


# @permission_classes([IsAuthenticated])
class EventosPorEstablecimientoView(APIView):
    """
    Vista para obtener eventos basados en el ID del establecimiento.
    """

    def get(self, request, pk_establecimiento):
        """
        Obtiene los eventos asociados a un establecimiento.
        """
        try:
            eventos = Evento.objects.filter(establecimiento_id=pk_establecimiento)
            serializer = EventoSerializer(eventos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# API de imagenes de Eventos
class ImagenesEventosView(APIView):
    # Recibe el id del Eventos al que se le asociará la imagen
    def post(self, request, pk):
        """
        Crea una nueva imagen asociada a un Evento.

        La estructura de debe ser un Form Data en la cual se pueden mandar varias imagenes a la vez. Ejemplo:
            imagen1: imagen1.jpg
            imagen2: imagen2.jpg
            ...
            imagen3: imagen3.jpg
        """

        

        try:
            evento = get_object_or_404(Evento, id=pk)
            imagenes_existentes = ImagenEvento.objects.filter(evento=evento).count()
            imagenes = [request.data.get(f'imagen{i}') for i in range(1, len(request.data)+1)]
            suma_imgenes_guardas_subidas = imagenes_existentes + len([imagen for imagen in imagenes if imagen])

            # Validar el tipo de archivo de las imágenes
            formatos_permitidos = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
            for imagen in imagenes:
                if imagen and imagen.content_type not in formatos_permitidos:
                    return Response(
                        {'detail': 'Formato de imagen no permitido. Solo se permiten imágenes JPEG, PNG, JPG o WebP.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if imagenes_existentes >= 3 or suma_imgenes_guardas_subidas > 3:
                return Response(
                    {'detail': 'El evento no puede tener más de 3 imágenes.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not any(imagenes):
                return Response(
                    {'detail': 'Debe proporcionar al menos una imagen.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            for imagen in imagenes:
                if imagen:
                    total_size_mb = imagen.size / (1024 * 1024)
                    if total_size_mb > 5:
                        return Response(
                                {'detail': 'El tamaño las imágenes no puede exceder los 5 MB.'},
                    status=status.HTTP_400_BAD_REQUEST)
                    else:
                        ImagenEvento.objects.create(evento=evento, imagen=imagen)
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
        Obtiene las imágenes asociadas a un evento.
        """
        try:
            evento = get_object_or_404(Evento, id=pk)
            imagenes = ImagenEvento.objects.filter(evento=evento)
            serializer = ImagenEventoSerializer(imagenes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk_imagen):
        """
        Elimina una imagen asociada a un evento.
        """
        try:
            imagen = get_object_or_404(ImagenEvento, id=pk_imagen)
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
    