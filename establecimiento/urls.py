from django.urls import path, include
from rest_framework import routers
from establecimiento import views

router = routers.DefaultRouter()
router.register(r'', views.EstablecimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]