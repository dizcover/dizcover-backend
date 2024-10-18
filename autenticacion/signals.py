from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

@receiver(user_logged_in)
def save_additional_user_data(sender, request, user, **kwargs):
    # Verificar si el usuario ha vinculado su cuenta social
    try:
        social_account = SocialAccount.objects.get(user=user)
    except SocialAccount.DoesNotExist:
        return  # Si no existe la cuenta social, no hacer nada
    
    # Extraer los datos de la cuenta social de Google
    extra_data = social_account.extra_data

    # Si el nombre completo no está presente, lo guardamos desde Google
    if not user.nombre_completo:
        user.nombre_completo = extra_data.get('name', '')

    # Guardar foto de perfil
    if not user.foto_perfil:
        user.foto_perfil = extra_data.get('picture', '')

    # Guardar fecha de nacimiento, si está disponible
    if not user.fecha_nacimiento and 'birthday' in extra_data:
        user.fecha_nacimiento = extra_data.get('birthday', '')

    # Guardar el usuario actualizado
    user.save()
