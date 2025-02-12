from django.core.management.base import BaseCommand
from establecimiento.models import Establecimiento
from eventos.models import Evento
from random import choice, randint
from faker import Faker
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Genera eventos aleatorios para los establecimientos existentes'

    def handle(self, *args, **kwargs):
        fake = Faker('es_CO')  # Genera datos específicos para Colombia
        
        # Obtener todos los establecimientos
        establecimientos = Establecimiento.objects.all()
        
        if not establecimientos.exists():
            self.stdout.write(self.style.ERROR("No hay establecimientos disponibles"))
            return
        
        for establecimiento in establecimientos:
            # Generamos entre 1 y 3 eventos por establecimiento
            num_eventos = randint(1, 3)
            
            for _ in range(num_eventos):
                # Generar datos aleatorios para cada evento
                nombre_evento = fake.word().capitalize() + " Party"  # Nombre del evento
                descripcion_evento = fake.paragraph(nb_sentences=2)  # Descripción del evento
                fecha_evento = fake.date_between(start_date="today", end_date="+30d")  # Fecha en los próximos 30 días
                lugar_evento = establecimiento.nombre  # Lugar del evento, que es el nombre del establecimiento
                reservas = randint(0, 100)  # Número aleatorio de reservas
                reservar = choice([True, False])  # Determina si es posible hacer una reserva

                # Crear el evento
                evento = Evento.objects.create(
                    nombre=nombre_evento,
                    fecha=fecha_evento,
                    descripcion=descripcion_evento,
                    reservar=reservar,
                    lugar=lugar_evento,
                    cantidad_reservas=reservas,
                    establecimiento=establecimiento
                )

                self.stdout.write(self.style.SUCCESS(f"Evento '{nombre_evento}' creado para el establecimiento '{establecimiento.nombre}'."))

        self.stdout.write(self.style.SUCCESS("Se crearon eventos para los establecimientos."))
