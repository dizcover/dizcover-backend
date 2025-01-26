from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy

from .managers import UserManager

class Users(AbstractBaseUser, PermissionsMixin):
    nombre_usuario = models.CharField(
        gettext_lazy("nombre_usuario"), max_length=30, unique=True, blank=False, null=False
    )
    email = models.EmailField(gettext_lazy("email address"), unique=True, blank=True, null=True)
    nombre_completo = models.CharField(
        gettext_lazy("nombre_completo"), max_length=100, blank=True, null=True
    )
    fecha_nacimiento = models.DateField(
        gettext_lazy("fecha_nacimiento"), blank=True, null=True
    )
    foto_perfil = models.CharField(
        gettext_lazy("foto_perfil"), max_length=200, blank=True, null=True
    )
    fecha_registro = models.DateTimeField(gettext_lazy("fecha_registro"), auto_now_add=True)

    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(gettext_lazy("active"), default=True)


    TIPO_CHOICES = [
        ('indefinido', 'Indefinido'),
        ('discotequero', 'Discotequero'),
        ('fiestero', 'Fiestero'),
    ]
    tipo = models.CharField(
        gettext_lazy("tipo"), max_length=20, choices=TIPO_CHOICES, default='indefinido', blank=True, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "nombre_usuario"
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = gettext_lazy("user")
        verbose_name_plural = gettext_lazy("users")

    def __str__(self):
        return self.nombre_usuario

    @property
    def full_name(self):
        return self.nombre_completo or self.nombre_usuario

    @property
    def user_type(self):
        if hasattr(self, 'fiestero'):
            return 'fiestero'
        elif hasattr(self, 'discotequero'):
            return 'discotequero'
        elif self.is_staff:
            return 'admin'
        else:
            return 'unknown'
