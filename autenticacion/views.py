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
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        user = request.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Datos básicos que se devuelven siempre al inicio
        data = {
            'user_id': user.pk,
            'email': user.email,
            'nombre_completo': user.nombre_completo,
            'foto_perfil': user.foto_perfil,
            'refresh_token': str(refresh),
            'access_token': access_token, 
            'tipo_usuario': user.tipo  # Mostrar el tipo actual del usuario
        }

        # Verificar si el usuario ya tiene un tipo asignado
        if user.tipo != 'indefinido':
            # El tipo ya está asignado, entonces mostramos la vista de login con la info del usuario
            if Fiestero.objects.filter(user=user).exists():
                tipo = 'fiestero'
                data['tipo_usuario'] = tipo
            elif Discotequero.objects.filter(user=user).exists():
                tipo = 'discotequero'
                data['tipo_usuario'] = tipo
            return render(request, 'login.html', {'data': data})
        
        # Si el usuario tiene el tipo 'indefinido', verificarlo a través de la API
        api_url = f"http://localhost:8000/autenticacion/verificacion-tipo-usuario/{user.pk}/"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.get(api_url, headers=headers)
            response_data = response.json()

            # Verificar la respuesta de la API
            if response.status_code == 200:
                if not response_data['value']:  # Si no tiene tipo de usuario asignado
                    return render(request, 'seleccion_tipo_usuario.html', {'data': data})  # Redirigir a la página de selección
                else:
                    # Si ya tiene un tipo asignado, mostrar el tipo
                    tipo_usuario = response_data['message']
                    data['tipo_usuario'] = tipo_usuario
                    return render(request, 'login.html', {'data': data})

        except requests.exceptions.RequestException as e:
            # Manejar errores de la solicitud
            print(f"Error al llamar a la API de verificación: {e}")
            return render(request, 'error.html', {'message': 'Error en la verificación del tipo de usuario'})

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')

# APIS



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def type_verification_user(request, pk_user):
    try:
        user = Users.objects.get(pk=pk_user)
        
        if Fiestero.objects.filter(user=user).exists():
            return Response({
                'message': 'El usuario es Fiestero',
                'value': True,
                'id': Fiestero.objects.get(user=user).pk
                
                }, status=status.HTTP_200_OK)
        elif Discotequero.objects.filter(user=user).exists():
            return Response({
                'message': 'El usuario es Discotequero',
                'value': True
                }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                'message': 'El usuario no tiene un tipo de usuario asignado',
                'value': False
                }, status=status.HTTP_200_OK)

    except Users.DoesNotExist:
        return Response({
            'message': 'Usuario no encontrado o no existe',
            }, status.HTTP_404_NOT_FOUND)

    
# API Usuarios
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        # Obtener el usuario autenticado
        user = request.user
        # Serializar la información del usuario
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def credenciales(request):
    user = request.user  # El usuario que ha iniciado sesión (autenticado con Google)
    
    if user.is_authenticated:
        # Generar tokens para el usuario
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Devolver los tokens y el id de usuario (que es el id de Django)
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user.id,  # Aquí devuelves el id del usuario de Django
            'user_type': user.tipo  # El tipo de usuario (si ya está asignado)
        })
    
    return Response({
        'message': 'El usuario no está autenticado correctamente'
    }, status=401)
        
    
    
@api_view(['POST'])
def seleccion_tipo_usuario(request):
    print(request.data)

    try:
        # Obtener el usuario
        user = Users.objects.get(pk=request.data['user_id'])

        # Comprobar si el tipo ya está definido, si es así, no permitir la actualización
        if user.tipo != 'indefinido':
            return Response({
                'message': 'El tipo de usuario ya está definido.',
                'tipo_usuario': user.tipo
            }, status=status.HTTP_400_BAD_REQUEST)

        tipo_usuario = request.data['tipo_usuario']

        # Dependiendo del tipo, se crea la instancia correspondiente
        if tipo_usuario == 'fiestero':
            identidad_genero = request.data['identidad_sexo']
            identificacion = request.data['identificacion']
            passaporte = request.data['passaporte']

            # Crear la instancia de Fiestero
            fiestero_a_crear = Fiestero.objects.create(
                user=user,
                identidad_sexo=identidad_genero,
                num_identificacion=identificacion,
                pasaporte=passaporte
            )

            fiesteroSerializer = FiesteroSerializer(fiestero_a_crear)
            
            # Actualizar el tipo del usuario
            user.tipo = 'fiestero'
            user.save()

            return Response({
                'message': 'Usuario Fiestero creado exitosamente',
                'data': fiesteroSerializer.data
            }, status=status.HTTP_201_CREATED)

        elif tipo_usuario == 'discotequero':
            nombre_empresarial = request.data['nombre_empresarial']
            NIT = request.data['nit']
            digito_verificacion = request.data['digito_verificacion_nit']

            # Crear la instancia de Discotequero
            discotequero_a_crear = Discotequero.objects.create(
                user=user,
                nombre_empresarial=nombre_empresarial,
                NIT=NIT,
                digito_verificacion=digito_verificacion,
            )

            discotequeroSerializer = DiscotequeroSerializer(discotequero_a_crear)
            
            # Actualizar el tipo del usuario
            user.tipo = 'discotequero'
            user.save()

            return Response({
                'message': 'Usuario Discotequero creado exitosamente',
                'data': discotequeroSerializer.data
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                'message': 'Tipo de usuario no válido'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Users.DoesNotExist:
        return Response({
            'message': 'Usuario no encontrado o no existe'
        }, status=status.HTTP_404_NOT_FOUND)
