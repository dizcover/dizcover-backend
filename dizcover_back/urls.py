from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from .views import home


# # Configuración del esquema de documentación
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Dizcover API Documentation",
#         default_version='v1',
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/evento/', include('eventos.urls')),
    path('api/discotequero/', include('discotequero.urls')),
    path('api/establecimiento/', include('establecimiento.urls')),
    path('api/fiestero/', include('fiestero.urls')),
    path('docs/', include_docs_urls(title='Dizcover API Documentation')),

    # path('docs/', include_docs_urls(title='Dizcover API Documentation')),
    path('api/autenticacion/', include('autenticacion.urls')), #Para la autenticacion
    path('accounts/', include('allauth.urls')), #Para la autenticacion con google
    path('', home),  # Ruta para la página de inicio en la raíz

]

