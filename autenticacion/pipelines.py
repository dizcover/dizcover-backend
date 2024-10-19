# pipelines.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


# CAda vez que el usuario inicie sesión con Google, Se actualizaŕa su información en dado caso que haya cambios en un correo de gmail
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)
        if sociallogin.is_existing:
            # Obtiene el usuario
            user = sociallogin.user
            
            # Extrae la información adicional del perfil de Google
            extra_data = sociallogin.account.extra_data
            print(extra_data)
            
            # Actualiza los campos del usuario
            user.nombre_completo = extra_data.get('name', user.nombre_completo)
            user.foto_perfil = extra_data.get('picture', user.foto_perfil)
            user.fecha_nacimiento = extra_data.get('birthdate', user.fecha_nacimiento)
            user.save()
