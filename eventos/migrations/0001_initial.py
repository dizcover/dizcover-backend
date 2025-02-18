# Generated by Django 5.1.1 on 2025-02-08 13:37

import django.db.models.deletion
import eventos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('establecimiento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField()),
                ('reservar', models.BooleanField(default=False)),
                ('lugar', models.CharField(max_length=100)),
                ('cantidad_reservas', models.IntegerField(default=0)),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='establecimiento.establecimiento')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(null=True, upload_to=eventos.models.upload_to_establecimiento)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='eventos.evento')),
            ],
        ),
    ]
