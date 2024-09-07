from django.urls import path, include
from rest_framework import routers
from fiestero import views

router = routers.DefaultRouter()
router.register(r'', views.FavoritoViewSet)

urlpatterns = [
    path('favoritos', include(router.urls)),
]