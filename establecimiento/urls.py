from django.urls import path, include
from rest_framework import routers
from establecimiento import views

router = routers.DefaultRouter()
router.register(r'', views.EstablecimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/imagenes/', views.ImagenesEstablecimientoView.as_view(), name='Crear Establecimiento'),
    path('imagenes/<int:pk_imagen>/', views.ImagenesEstablecimientoView.as_view(), name='Crear Imagen'),


    # Horario
    path('<int:pk>/horarios/', views.HorarioEstablecimientoView.as_view(), name='Crear y Obtener Horario'),
    path('horario/<int:pk>/', views.HorarioEstablecimientoView.as_view(), name='eliminar y actualizar dia horario'),

    # Coordenada
    path('<int:pk>/coordenadas/', views.CoordenadaEstablecimientoView.as_view(), name='Coordenada'),
    path('<int:pk>/coordenadas/<int:coord_pk>', views.CoordenadaEstablecimientoView.as_view(), name='Eliminar y Actualizar Coordenada'),
]