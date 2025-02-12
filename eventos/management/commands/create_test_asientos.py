import random
from django.core.management.base import BaseCommand
from eventos.models import Evento, Asiento
from decimal import Decimal

class Command(BaseCommand):
    help = 'Genera asientos aleatorios para los eventos existentes'

    def handle(self, *args, **kwargs):
        eventos = Evento.objects.all()  # Obtener todos los eventos

        for evento in eventos:
            # Generar entre 0 y 4 asientos para cada evento
            num_asientos = random.randint(0, 4)
            
            for _ in range(num_asientos):
                # Definir los nombres de los asientos
                nombre_asiento = random.choice(['Premium', 'Normal', 'VIP', 'General'])
                # Definir un precio aleatorio entre 50000 y 150000
                precio = random.choice([Decimal('50000.00'), Decimal('100000.00'), Decimal('150000.00')])
                # Definir una cantidad de cupos aleatoria entre 20 y 100
                cupos = random.randint(20, 100)

                # Crear el asiento para el evento
                Asiento.objects.create(evento=evento, nombre=nombre_asiento, precio=precio, cupos=cupos)

            self.stdout.write(self.style.SUCCESS(f'Asientos generados para el evento "{evento.nombre}"'))
