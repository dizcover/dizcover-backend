from django.db import migrations
import json
from django.conf import settings
from recomendacion.models import Etiqueta

def load_etiquetas(apps, schema_editor):
    # Ruta del archivo JSON
    json_file_path = 'recomendacion/etiquetas.json'

    try:
        # Abrir y cargar el archivo JSON
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Etiquetas Genero
        for etiqueta in data.get('etiquetas-genero', []):
            if not Etiqueta.objects.filter(nombre=etiqueta, tipo=Etiqueta.GENERO).exists():
                Etiqueta.objects.create(nombre=etiqueta, tipo=Etiqueta.GENERO)

        # Etiquetas Ambiente
        for etiqueta in data.get('etiquetas-ambiente', []):
            if not Etiqueta.objects.filter(nombre=etiqueta, tipo=Etiqueta.AMBIENTE).exists():
                Etiqueta.objects.create(nombre=etiqueta, tipo=Etiqueta.AMBIENTE)

        # Etiquetas Especiales
        for etiqueta in data.get('etiquetas-especiales', []):
            if not Etiqueta.objects.filter(nombre=etiqueta, tipo=Etiqueta.ESPECIAL).exists():
                Etiqueta.objects.create(nombre=etiqueta, tipo=Etiqueta.ESPECIAL)

    except Exception as e:
        print(f'Error al cargar las etiquetas: {e}')

class Migration(migrations.Migration):

    dependencies = [
        ('recomendacion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_etiquetas),
    ]
