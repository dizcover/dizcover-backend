# Generated by Django 5.1.1 on 2025-01-15 17:13

import establecimiento.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establecimiento', '0004_remove_establecimiento_imagen_imagenestablecimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenestablecimiento',
            name='imagen',
            field=models.FileField(null=True, upload_to=establecimiento.models.upload_to_establecimiento),
        ),
    ]
