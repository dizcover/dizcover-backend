from django.urls import path, include
from rest_framework import routers
from eventos import views

router = routers.DefaultRouter()
router.register(r'', views.EventoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('establecimiento/<int:pk_establecimiento>', views.EventosPorEstablecimientoView.as_view(), name='Eventos por establecimiento'),
    path('<int:pk>/imagenes/', views.ImagenesEventosView.as_view(), name='Crear imagen evento'),
    path('imagenes/<int:pk_imagen>/', views.ImagenesEventosView.as_view(), name='obtener imagen evento'),
    path('asientos/<int:pk>/', views.AsientosEventoView.as_view(), name='Asientos por evento'),
]