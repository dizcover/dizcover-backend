from django.urls import path, include
from rest_framework import routers
from establecimiento import views

router = routers.DefaultRouter()
router.register(r'', views.EstablecimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/imagenes/', views.ImagenesEstablecimientoView.as_view(), name='Crear Establecimiento'),
    path('imagenes/<int:pk_imagen>/', views.ImagenesEstablecimientoView.as_view(), name='Crear Establecimiento'),
]