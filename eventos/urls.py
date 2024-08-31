from django.urls import path, include
from rest_framework import routers
from eventos import views

router = routers.DefaultRouter()
router.register(r'', views.EventoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]