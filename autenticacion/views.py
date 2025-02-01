from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from autenticacion.models import Users
from fiestero.models import Fiestero
from discotequero.models import Discotequero
from rest_framework import status
import requests
from autenticacion.serializer import UserSerializer
from fiestero.serializer import FiesteroSerializer
from discotequero.serializer import DiscotequeroSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes



def login_view(request):
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        user = request.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Datos que puedes pasar al template
        data = {
            'user_id': user.pk,
            'email': user.email,
            'nombre_completo': user.nombre_completo,
            'foto_perfil': user.foto_perfil,
            'refresh_token': str(refresh),
            'access_token': access_token, 
            'tipo_usuario': user.tipo
        }

        # Si el tipo de usuario está definido
        if user.tipo != 'indefinido':
            return render(request, 'login.html', {'data': data, 'show_selection_button': False})

        # Si el tipo de usuario no está definido, mostramos un botón para elegir
        return render(request, 'login.html', {'data': data, 'show_selection_button': True})

    # Si el usuario no está autenticado, redirigir a la autenticación de Google
    return redirect("http://localhost:8000/accounts/google/login/?process=login")

def logout_view(request):
    logout(request)
    return redirect('login')

def seleccion_vista(request):
    if request.user.is_authenticated:
        user = request.user
        
        # Datos básicos que se devuelven siempre al inicio
        data = {
            'user_id': user.pk,
            'email': user.email,
            'nombre_completo': user.nombre_completo,
            'foto_perfil': user.foto_perfil,
            'tipo_usuario': user.tipo  # Mostrar el tipo actual del usuario
        }

    return render(request, 'seleccion_tipo_usuario.html', {'data': data})

# APIS

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_tipo_usuario(request, id_user):
    """
    Verifica si el usuario tiene un tipo asignado. Si no, redirige al frontend para que elija el tipo.
    """
    user = Users.objects.get(pk=id_user)
    if user.tipo == 'indefinido':
        # Si el tipo es 'indefinido', redirigir al frontend para que elija el tipo
        return Response({'message': 'Tipo de usuario no asignado', 'valor': False}, status=status.HTTP_200_OK)
    else:
        # Si ya tiene un tipo de usuario, devolver la información
        return Response({'message': 'Usuario tiene tipo asignado', 'user_type': user.tipo}, status=status.HTTP_200_OK)

#Este deberia ser la unica vista que NO esta recibiendo credenciales ya que las genera. Los univos credenciales que se deben recibir 
@api_view(['POST'])
def generar_token_jwt(request):
    try:
        # Obtener el usuario autenticado con Google
        user = request.user
        # Generar los tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        data = {
            'access_token': access_token,
            'refresh_token': str(refresh),
            'user_id': user.id,
            'tipo_usuario': user.tipo
        }

        # Responder con los tokens generados
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seleccion_tipo_usuario(request, id_user):
    """
    Asigna un tipo de usuario a un usuario recién autenticado (fiestero o discotequero).
            """
    try:
        # Obtener el usuario
        user = Users.objects.get(pk=id_user)

        # Comprobar si el tipo ya está definido, si es así, no permitir la actualización
        if user.tipo != 'indefinido':
            return Response({
                'message': 'El tipo de usuario ya está definido.',
                'tipo_usuario': user.tipo
            }, status=status.HTTP_400_BAD_REQUEST)

        tipo_usuario = request.data['tipo_usuario']

        # Dependiendo del tipo, se crea la instancia correspondiente
        if tipo_usuario == 'fiestero':
            fiestero_data = {
                'user': user.id,
                'identidad_sexo': request.data['identidad_sexo'],
                'num_identificacion': request.data['identificacion'],
                'pasaporte': request.data['passaporte']
            }

            # Validar y crear la instancia de Fiestero usando el serializer
            fiestero_serializer = FiesteroSerializer(data=fiestero_data)
            if fiestero_serializer.is_valid():
                fiestero_serializer.save()
                user.tipo = 'fiestero'
                user.save()
                return Response({
                    'message': 'Usuario Fiestero creado exitosamente',
                    'data': {'user_id': user.id, 'tipo_usuario': 'fiestero'}
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(fiestero_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif tipo_usuario == 'discotequero':
            discotequero_data = {
                'user': user.id,
                'nombre_empresarial': request.data['nombre_empresarial'],
                'NIT': request.data['nit'],
                'digito_verificacion': request.data.get('numero_verificacio')
            }

            # Validar y crear la instancia de Discotequero usando el serializer
            discotequero_serializer = DiscotequeroSerializer(data=discotequero_data)
            if discotequero_serializer.is_valid():
                discotequero_serializer.save()
                user.tipo = 'discotequero'
                user.save()
                return Response({
                     'message': 'Usuario Discotequero creado exitosamente',
                      'data': {'user_id': user.id, 'tipo_usuario': 'discotequero'}
                }, status=status.HTTP_201_CREATED)
            else:
                  return Response(discotequero_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
             return Response({
                'message': 'Tipo de usuario no válido'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Users.DoesNotExist:
        return Response({
            'message': 'Usuario no encontrado, atributos incorrectos o tipo de usuario no válido.'
         }, status=status.HTTP_404_NOT_FOUND)

    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, id_user):
        # Obtener el usuario autenticado
        
        user = Users.objects.get(pk=id_user)
        # Serializar la información del usuario
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id_user):
        try:
            user = Users.objects.get(pk=id_user)
            user.delete()
            return Response({'message': 'Usuario eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)
        except Users.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

class TokenRefresco(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, id_user):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token es necesario.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verificar y decodificar el refresh token
            refresh = RefreshToken(refresh_token)
            print(refresh['user_id'])
            # Verificar que el token corresponde al usuario
            if refresh['user_id'] != id_user:
                print(refresh)
                return Response({'detail': 'El refresh token no corresponde al usuario.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generar nuevos tokens
            access_token = str(refresh.access_token)

            return Response({
                'access_token': access_token,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    