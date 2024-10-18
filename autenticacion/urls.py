from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # API

    path('verificacion-tipo-usuario/<int:pk_user>/', views.type_verification_user, name='type_verification_user'),
    path('seleccion-tipo-usuario/', views.seleccion_tipo_usuario, name='seleccion_tipo_usuario'),

]
