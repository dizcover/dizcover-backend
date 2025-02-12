from django.core.management.base import BaseCommand
from fiestero.models import Fiestero
from establecimiento.models import Establecimiento
from fiestero.models import FeedBack, CalificacionEnum
from random import randint  
import random  
from faker import Faker

class Command(BaseCommand):
    help = 'Genera feedbacks aleatorios de los fiesteros para los establecimientos'

    def handle(self, *args, **kwargs):
        fake = Faker('es_CO')  # Faker para generar datos en español y de Colombia

        fiesteros = Fiestero.objects.all()
        establecimientos = Establecimiento.objects.all()

        if not fiesteros.exists():
            self.stdout.write(self.style.ERROR("No hay fiesteros disponibles"))
            return

        if not establecimientos.exists():
            self.stdout.write(self.style.ERROR("No hay establecimientos disponibles"))
            return

        # Generar entre 1 y 5 feedbacks por fiestero
        for fiestero in fiesteros:
            # Elegir entre 1 y 3 establecimientos aleatorios para este fiestero
            establecimientos_seleccionados = random.sample(list(establecimientos), randint(1, 3))
            
            for establecimiento in establecimientos_seleccionados:
                # Calificación aleatoria entre 1 y 5
                calificacion = randint(1, 5)
                
                # Generar un comentario aleatorio con Faker
                comentario = fake.text(max_nb_chars=500) if randint(0, 1) else None  # 50% chance de tener comentario
                
                # Crear el feedback
                feedback, created = FeedBack.objects.get_or_create(
                    fiestero=fiestero,
                    establecimiento=establecimiento,
                    defaults={
                        'calificacion': calificacion,
                        'comentario': comentario
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Feedback creado para el fiestero '{fiestero.user.nombre_usuario}' en el establecimiento '{establecimiento.nombre}'."))

        self.stdout.write(self.style.SUCCESS("Se generaron feedbacks aleatorios para los fiesteros y establecimientos."))
