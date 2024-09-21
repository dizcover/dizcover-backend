from django.contrib import admin
from .models import Establecimiento, Coordenada, Horario

# Register your models here.
admin.site.register(Establecimiento)
admin.site.register(Coordenada)
admin.site.register(Horario)