# Generated by Django 5.1.1 on 2025-02-01 21:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiestero', '0003_alter_fiestero_identidad_sexo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(blank=True, max_length=500, null=True)),
                ('calificacion', models.IntegerField(choices=[(1, '1 Estrella'), (2, '2 Estrellas'), (3, '3 Estrellas'), (4, '4 Estrellas'), (5, '5 Estrellas')], default=1)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('fiestero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fiestero.fiestero')),
            ],
        ),
    ]
