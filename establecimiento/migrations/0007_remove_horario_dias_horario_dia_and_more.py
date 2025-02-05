# Generated by Django 5.1.1 on 2025-01-18 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establecimiento', '0006_remove_establecimiento_id_coordenada_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horario',
            name='dias',
        ),
        migrations.AddField(
            model_name='horario',
            name='dia',
            field=models.CharField(choices=[('LUNES', 'Lunes'), ('MARTES', 'Martes'), ('MIERCOLES', 'Miércoles'), ('JUEVES', 'Jueves'), ('VIERNES', 'Viernes'), ('SABADO', 'Sábado'), ('DOMINGO', 'Domingo')], default='LUNES', max_length=20),
        ),
        migrations.CreateModel(
            name='HorarioEstablecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='establecimiento.establecimiento')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establecimiento.horario')),
            ],
        ),
    ]
