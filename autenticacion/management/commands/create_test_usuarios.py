from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fiestero.models import Fiestero
from discotequero.models import Discotequero
from random import choice, randint
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    help = 'Genera usuarios de prueba (fiesteros y discotequeros)'

    def handle(self, *args, **kwargs):
        for i in range(10):
            nombre_usuario = f'fiestero{i+1}'
            email = f'fiestero{i+1}@example.com'
            password = get_random_string(length=8)  
            usuario = User.objects.create_user(
                nombre_usuario=nombre_usuario,
                email=email,
                password=password,
                tipo='fiestero'
            )
            # Crear el perfil de Fiestero asociado
            Fiestero.objects.create(
                user=usuario,
                identidad_sexo=choice(['M', 'F', 'NB', 'O', 'PND']),
                num_identificacion=str(randint(100000000, 999999999)),  
                pasaporte=get_random_string(10, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')  
            )
        
        # Generamos 10 usuarios de tipo Discotequero
        for i in range(10):
            # Crear un usuario base
            nombre_usuario = f'discotequero{i+1}'
            email = f'discotequero{i+1}@example.com'
            password = get_random_string(length=8)  
            usuario = User.objects.create_user(
                nombre_usuario=nombre_usuario,
                email=email,
                password=password,
                tipo='discotequero'
            )
            # Crear el perfil de Discotequero asociado
            Discotequero.objects.create(
                user=usuario,
                nombre_empresarial=f'Empresa {i+1}',
                NIT=f'{randint(100000000, 999999999)}',
                NIT_verificado=choice([True, False]),
                numero_verificacion=get_random_string(10, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            )

        self.stdout.write(self.style.SUCCESS("Usuarios creados exitosamente."))