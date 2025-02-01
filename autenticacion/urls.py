from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), #Editar backend
    path('logout/', views.logout_view, name='logout'),#Editar backend
    path('seleccion/', views.seleccion_vista, name='Selección'),


    # API
    path('verificacion-tipo-usuario/', views.verificar_tipo_usuario, name='type_verification_user'),
    path('seleccion-tipo-usuario/<int:id_user>', views.seleccion_tipo_usuario, name='seleccion_tipo_usuario'),
    path('credenciales_jwt/', views.generar_token_jwt, name='seleccion_tipo_usuario'),
    path('usuario/<int:id_user>', views.UserProfileView.as_view(), name='usuario'),
    path('usuario/refrescar_token/<int:id_user>', views.TokenRefresco.as_view(), name='refrescar'),


]
