# Generated by Django 5.1.1 on 2025-01-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_evento_establecimiento_evento_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='eventos/eventosImages'),
        ),
    ]
