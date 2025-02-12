from django.core.management.base import BaseCommand
from discotequero.models import Discotequero
from establecimiento.models import Establecimiento
from random import choice
from faker import Faker

class Command(BaseCommand):
    help = 'Genera 15 establecimientos para los discotequero existentes con datos de Medellín y sus alrededores'

    def handle(self, *args, **kwargs):
        fake = Faker('es_CO')  # Especifica que se generen datos en formato colombiano
        
        # Lista de municipios específicos para Medellín y alrededores
        municipios_medellin_y_alrededores = [
            "Medellín", "Envigado", "Itagüí", "Sabaneta", "Bello", "La Estrella", 
            "Copacabana", "Girardota", "Barbosa", "San Vicente", "Caldas", "Rio Negro", 
            "Rionegro", "El Retiro", "La Ceja", "Marinilla", "El Santuario", "Guarne", 
            "Abejorral", "Concepción", "Amagá"
        ]
        
        # Departamentos relacionados con Medellín
        departamentos = [
            "Antioquia"
        ]
        
        # Obtener todos los discotequeros
        discotequeros = Discotequero.objects.all()
        
        if not discotequeros.exists():
            self.stdout.write(self.style.ERROR("No hay discotequeros disponibles"))
            return
        for i in range(15):
            # Seleccionar un discotequero aleatorio
            discotequero = choice(discotequeros)


            nombre = fake.company()  # Nombre de la empresa (ej. discoteca o bar)
            direccion = fake.address().replace("\n", " ")  # Dirección
            telefono = fake.phone_number()  # Número de teléfono
            email = fake.email()  # Email
            descripcion = fake.paragraph(nb_sentences=3)  # Descripción
            departamento = choice(departamentos)  # Seleccionar el departamento de Antioquia
            municipio = choice(municipios_medellin_y_alrededores)  # Seleccionar un municipio de Medellín o sus alrededores

            # Crear el establecimiento
            establecimiento = Establecimiento.objects.create(
                id_discotequero=discotequero,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email=email,
                descripcion=descripcion,
                departamento=departamento,
                municipio=municipio,
            )

            self.stdout.write(self.style.SUCCESS(f"Establecimiento '{nombre}' creado para el discotequero {discotequero.user.nombre_usuario}."))
        
        self.stdout.write(self.style.SUCCESS("Se crearon 15 establecimientos para los discotequeros en Medellín y alrededores."))
