from django.core.management.base import BaseCommand
from establecimiento.models import Establecimiento, HorarioEstablecimiento, Horario
from random import randint, choice
from datetime import time
from fiestero.models import Fiestero
from establecimiento.models import DiaSemanaEnum


class Command(BaseCommand):
    help = 'Genera horarios aleatorios para los establecimientos'

    def handle(self, *args, **kwargs):
        # Días posibles para los horarios
        dias = [dia.name for dia in DiaSemanaEnum]

        # Horarios típicos de apertura y cierre
        horarios_comunes = {
            DiaSemanaEnum.LUNES.name: ('20:00', '00:00'),  # Lunes (horario más corto)
            DiaSemanaEnum.MARTES.name: ('20:00', '00:00'),  # Martes (horario más corto)
            DiaSemanaEnum.MIERCOLES.name: ('20:00', '00:00'),  # Miércoles (horario más corto)
            DiaSemanaEnum.JUEVES.name: ('20:00', '01:00'),  # Jueves (algo más largo)
            DiaSemanaEnum.VIERNES.name: ('22:00', '04:00'),  # Viernes (horario largo)
            DiaSemanaEnum.SABADO.name: ('22:00', '04:00'),  # Sábado (horario largo)
            DiaSemanaEnum.DOMINGO.name: ('22:00', '03:00'),  # Domingo (horario largo)
        }

        # Recorrer los establecimientos
        for establecimiento in Establecimiento.objects.all():
            # Crear horarios aleatorios para cada establecimiento
            for dia in dias:
                apertura, cierre = horarios_comunes[dia]  # Obtener el horario base
                hora_apertura = time(int(apertura.split(':')[0]), int(apertura.split(':')[1]))
                hora_cierre = time(int(cierre.split(':')[0]), int(cierre.split(':')[1]))

                # Variar ligeramente los horarios de apertura y cierre de manera aleatoria para hacerlo más realista
                if dia in [DiaSemanaEnum.VIERNES.name, DiaSemanaEnum.SABADO.name]:
                    # Los fines de semana pueden variar más
                    hora_apertura = time(randint(21, 23), randint(0, 59))  # Aleatorio entre 9 PM y 11 PM
                    hora_cierre = time(randint(2, 4), randint(0, 59))  # Aleatorio entre 2 AM y 4 AM
                else:
                    # Días de semana (Lunes a Jueves) con horarios más limitados
                    hora_apertura = time(randint(19, 21), randint(0, 59))  # Aleatorio entre 7 PM y 9 PM
                    hora_cierre = time(randint(0, 1), randint(0, 59))  # Aleatorio entre 12 AM y 1 AM

                # Crear un nuevo objeto Horario para cada día del establecimiento
                horario = Horario.objects.create(
                    dia=dia,
                    hora_apertura=hora_apertura,
                    hora_cierre=hora_cierre,
                )

                # Crear la relación entre Establecimiento y Horario
                HorarioEstablecimiento.objects.create(
                    establecimiento=establecimiento,
                    horario=horario
                )

            self.stdout.write(self.style.SUCCESS(f"Horarios generados para el establecimiento {establecimiento.nombre}"))
        
        self.stdout.write(self.style.SUCCESS("Horarios generados para todos los establecimientos."))
