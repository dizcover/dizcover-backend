from django.urls import path, include
from rest_framework import routers
from fiestero import views


urlpatterns = [
    path('<int:fiestero_id>/favoritos/', views.FavoritoViewSet.as_view(), name='Favoritos'),
    path('<int:fiestero_id>/favoritos/<int:establecimiento_id>/', views.verificar_favorito_establecimiento, name='Favoritos'),

    path('<int:establecimiento_id>/feedback/', views.FeedBackView.as_view(), name='crear_feedback'),
    path('feedback/<int:feedback_id>/', views.FeedBackView.as_view(), name='eliminar_feedback'),
    path('<int:establecimiento_id>/feedbacks/', views.FeedBackView.as_view(), name='obtener_feedbacks'),
]