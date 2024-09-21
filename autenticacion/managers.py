from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """Override of BaseUserManager for our Custom User in system"""

    use_in_migrations = True

    def _create_user(self, nombre_usuario, password, **extra_fields):
        """help method for create a user"""
        if not nombre_usuario:
            raise ValueError("El nombre de usuario debe ser establecido")
        user = self.model(nombre_usuario=nombre_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nombre_usuario, password=None, **extra_fields):
        """
        Create a normal user, with minimum required args:
        nombre_usuario, password
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(nombre_usuario, password, **extra_fields)

    def create_superuser(self, nombre_usuario, password=None, **extra_fields):
        """
        Create a super user (root), with minimum required args:
        nombre_usuario, password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # extra_fields.setdefault("user_type", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(nombre_usuario, password, **extra_fields)