from django.core.management.base import BaseCommand
from establecimiento.models import Establecimiento
from fiestero.models import Fiestero
from recomendacion.models import Etiqueta, EtiquetaEstablecimiento, EtiquetasFiestero
from random import sample, randint
from faker import Faker

class Command(BaseCommand):
    help = 'Genera etiquetas aleatorias para establecimientos y fiesteros'

    def handle(self, *args, **kwargs):
        fake = Faker('es_CO')  # Datos en español y de Colombia
        
        # Obtener todas las etiquetas existentes
        etiquetas = Etiqueta.objects.all()

        if not etiquetas.exists():
            self.stdout.write(self.style.ERROR("No hay etiquetas disponibles"))
            return
        
        # Asignar etiquetas aleatorias a los establecimientos
        establecimientos = Establecimiento.objects.all()
        
        if not establecimientos.exists():
            self.stdout.write(self.style.ERROR("No hay establecimientos disponibles"))
            return

        for establecimiento in establecimientos:
            num_etiquetas = randint(2, 5)  # Asignar entre 2 y 5 etiquetas
            etiquetas_aleatorias = sample(list(etiquetas), num_etiquetas)  # Seleccionar aleatoriamente las etiquetas
            
            for etiqueta in etiquetas_aleatorias:
                # Crear la relación entre el establecimiento y las etiquetas seleccionadas
                if not EtiquetaEstablecimiento.objects.filter(etiqueta=etiqueta, establecimiento=establecimiento).exists():
                    EtiquetaEstablecimiento.objects.create(etiqueta=etiqueta, establecimiento=establecimiento)

            self.stdout.write(self.style.SUCCESS(f"{num_etiquetas} etiquetas asignadas al establecimiento '{establecimiento.nombre}'."))

        # Asignar etiquetas aleatorias a los fiesteros
        fiesteros = Fiestero.objects.all()
        
        if not fiesteros.exists():
            self.stdout.write(self.style.ERROR("No hay fiesteros disponibles"))
            return

        for fiestero in fiesteros:
            num_etiquetas = randint(1, 3)  # Asignar entre 1 y 3 etiquetas
            etiquetas_aleatorias = sample(list(etiquetas), num_etiquetas)  # Seleccionar aleatoriamente las etiquetas
            
            for etiqueta in etiquetas_aleatorias:
                # Crear la relación entre el fiestero y las etiquetas seleccionadas
                if not EtiquetasFiestero.objects.filter(etiqueta=etiqueta, fiestero=fiestero).exists():
                    EtiquetasFiestero.objects.create(etiqueta=etiqueta, fiestero=fiestero)

            self.stdout.write(self.style.SUCCESS(f"{num_etiquetas} etiquetas asignadas al fiestero '{fiestero.user.nombre_usuario}'."))

        self.stdout.write(self.style.SUCCESS("Se generaron etiquetas aleatorias para establecimientos y fiesteros."))
