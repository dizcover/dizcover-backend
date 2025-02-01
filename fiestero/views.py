from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
from .models import Favorito, Fiestero, FeedBack
from establecimiento.models import Establecimiento
from .serializer import FavoritotoSerializer, FeedBackSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class FavoritoViewSet(APIView):
    """
    Vista para gestionar los favoritos de un fiestero.
    """

    def get_fiestero(self, fiestero_id):
        """Obtiene el fiestero a partir del id"""
        return get_object_or_404(Fiestero, id=fiestero_id)

    def get_establecimiento(self, establecimiento_id):
        """Obtiene el establecimiento a partir del id"""
        return get_object_or_404(Establecimiento, id=establecimiento_id)

    def post(self, request, fiestero_id):
        """
        Crea un nuevo favorito solo si no existe uno previamente para el mismo fiestero y establecimiento.
        """
        establecimiento_id = request.data.get('establecimiento')

        if not establecimiento_id:
            return Response(
                {'detail': 'Debe proporcionar el id del establecimiento.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener fiestero
        fiestero = self.get_fiestero(fiestero_id)

        # Obtener establecimiento
        establecimiento = self.get_establecimiento(establecimiento_id)

        # Verificar si ya existe este favorito
        if Favorito.objects.filter(fiestero=fiestero, establecimiento=establecimiento).exists():
            return Response(
                {'detail': 'Este establecimiento ya está marcado como favorito por este usuario.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear el favorito
        favorito = Favorito.objects.create(fiestero=fiestero, establecimiento=establecimiento)

        # Serializar el favorito creado
        serializer = FavoritotoSerializer(favorito)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, fiestero_id):
        """
        Lista los favoritos de un fiestero basado en su id que se pasa en la URL.
        """
        fiestero = self.get_fiestero(fiestero_id)

        # Obtener favoritos de este fiestero
        favoritos = Favorito.objects.filter(fiestero=fiestero)

        # Serializar los favoritos
        serializer = FavoritotoSerializer(favoritos, many=True)
        return Response(serializer.data)

    def delete(self, request, fiestero_id):
        """
        Elimina un favorito basado en el id del fiestero y el id del establecimiento.
        """
        establecimiento_id = request.data.get('establecimiento')

        if not establecimiento_id:
            return Response(
                {'detail': 'Debe proporcionar el id del establecimiento.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener fiestero
        fiestero = self.get_fiestero(fiestero_id)

        # Obtener establecimiento
        establecimiento = self.get_establecimiento(establecimiento_id)

        # Buscar el favorito
        favorito = get_object_or_404(Favorito, fiestero=fiestero, establecimiento=establecimiento)

        # Eliminar el favorito
        favorito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeedBackView(APIView):
    
    def post(self, request, establecimiento_id):
        """
        Crea un nuevo feedback para un establecimiento especificado.
        """
        fiestero_id = request.data.get('fiestero')
        comentario = request.data.get('comentario')
        calificacion = request.data.get('calificacion')

        if not fiestero_id or not comentario or not calificacion:
            return Response(
                {'detail': 'Debe proporcionar fiestero, comentario y calificación.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fiestero = Fiestero.objects.get(id=fiestero_id)
            establecimiento = Establecimiento.objects.get(id=establecimiento_id)

            # Verificar si el fiestero ya tiene un feedback para este establecimiento
            if FeedBack.objects.filter(fiestero=fiestero, establecimiento=establecimiento).exists():
                return Response(
                    {'detail': 'El fiestero ya ha dejado un comentario para este establecimiento.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear el feedback
            feedback = FeedBack.objects.create(
                fiestero=fiestero,
                establecimiento=establecimiento,
                comentario=comentario,
                calificacion=calificacion,
            )

            # Serializar y devolver el feedback creado
            serializer = FeedBackSerializer(feedback)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Fiestero.DoesNotExist:
            return Response({'detail': 'Fiestero no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Establecimiento.DoesNotExist:
            return Response({'detail': 'Establecimiento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, establecimiento_id):
        """
        Obtiene todos los feedbacks de un establecimiento específico.
        """
        try:
            establecimiento = Establecimiento.objects.get(id=establecimiento_id)
            feedbacks = FeedBack.objects.filter(establecimiento=establecimiento)
            serializer = FeedBackSerializer(feedbacks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Establecimiento.DoesNotExist:
            return Response({'detail': 'Establecimiento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, feedback_id):
        """
        Elimina un feedback específico para un establecimiento y un fiestero.
        """
        try:
            feedback = FeedBack.objects.get(id=feedback_id)
            feedback.delete()
            return Response({'detail': 'Feedback eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
        except FeedBack.DoesNotExist:
            return Response({'detail': 'Feedback no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)