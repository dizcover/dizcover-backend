# Generated by Django 5.1.1 on 2025-01-18 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establecimiento', '0005_alter_imagenestablecimiento_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='establecimiento',
            name='id_coordenada',
        ),
        migrations.RemoveField(
            model_name='establecimiento',
            name='id_horario',
        ),
    ]
