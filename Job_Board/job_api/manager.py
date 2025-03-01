from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, email, password=None, full_name=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, full_name=None, phone_number=None, **extra_fields):
        """
        Creates and saves a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be staff'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be superuser'))
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_('Superuser must be verified'))

        return self.create_user(email, password, full_name=full_name, phone_number=phone_number, **extra_fields)

