from recomendacion import views
from django.urls import path

urlpatterns = [
    path('etiquetas/', views.EtiquetasView.as_view(), name='etiquetas'),
    path('etiquetas/establecimiento/<int:pk>/', views.EstablecimientoEtiquetasView.as_view(), name='etiquetas_establecimiento'),
    path('etiquetas/fiestero/<int:pk_fiestero>/', views.EtiquetasFiesteroApi.as_view(), name='etiquetas_fiestero'),
]
