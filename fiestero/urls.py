from django.urls import path, include
from rest_framework import routers
from fiestero import views


urlpatterns = [
    path('<int:fiestero_id>/favoritos/', views.FavoritoViewSet.as_view(), name='Favoritos'),
]