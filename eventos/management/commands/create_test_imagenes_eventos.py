import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from eventos.models import Evento, ImagenEvento
from django.conf import settings

class Command(BaseCommand):
    help = 'Asigna imágenes aleatorias a los eventos'

    def handle(self, *args, **kwargs):
        # Ruta de las imágenes de prueba en la carpeta de eventos
        carpeta_imagenes_prueba = os.path.join(settings.BASE_DIR, 'eventos', 'imagenes_prueba')
        
        # Obtener las imágenes disponibles en la carpeta
        imagenes_prueba = [img for img in os.listdir(carpeta_imagenes_prueba) if img.endswith(('.png', '.jpg', '.jpeg'))]

        # Verificar si hay imágenes disponibles
        if not imagenes_prueba:
            self.stdout.write(self.style.ERROR('No hay imágenes disponibles en la carpeta de prueba.'))
            return

        # Obtener todos los eventos
        eventos = Evento.objects.all()

        # Asignar aleatoriamente una imagen de prueba a cada evento
        for evento in eventos:
            # Seleccionar una imagen aleatoria
            imagen_aleatoria = random.choice(imagenes_prueba)

            # Crear una instancia de ImagenEvento y asociarla al evento
            with open(os.path.join(carpeta_imagenes_prueba, imagen_aleatoria), 'rb') as img_file:
                imagen_evento = ImagenEvento(evento=evento)
                imagen_evento.imagen.save(imagen_aleatoria, File(img_file), save=True)

            # Confirmar la asignación
            self.stdout.write(self.style.SUCCESS(f'Imagen "{imagen_aleatoria}" asignada al evento "{evento.nombre}".'))


