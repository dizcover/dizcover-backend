from rest_framework import viewsets
from .serializer import EventoSerializer
from .models import Evento
from rest_framework.permissions import IsAuthenticated

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


    