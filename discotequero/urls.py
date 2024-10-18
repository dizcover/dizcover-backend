from django.urls import path, include
from rest_framework import routers
from discotequero import views

router = routers.DefaultRouter()
router.register(r'', views.DicotequeroViewSet)

urlpatterns = [
    path('', include(router.urls)),
]