from django.contrib import admin
from .models import Establecimiento, Coordenada, HorarioEstablecimiento, Horario, ImagenEstablecimiento

# Register your models here.
admin.site.register(Establecimiento)
admin.site.register(ImagenEstablecimiento)
admin.site.register(Coordenada)
admin.site.register(Horario)
admin.site.register(HorarioEstablecimiento)