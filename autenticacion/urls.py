from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), #Editar backend
    path('logout/', views.logout_view, name='logout'),#Editar backend


    # API
    path('verificacion-tipo-usuario/<int:pk_user>/', views.type_verification_user, name='type_verification_user'), #Implementar en frontend
    path('seleccion-tipo-usuario/', views.seleccion_tipo_usuario, name='seleccion_tipo_usuario'), #Implemnetar en frontend

    # API
    path('usuario', views.UserProfileView.as_view(), name='usuario'),
    path('usuario/credenciales/', views.credenciales, name='usuario'),

]
