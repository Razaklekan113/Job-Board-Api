# job_api/manager.py
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """
    def create_user(self, email, password=None, username=None, mobile_number=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        if not username and not mobile_number:
            raise ValueError(_('Either username or phone_number must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, username=None, mobile_number=None, **extra_fields):
        """
        Creates and saves a superuser.
        """
        if not username and not mobile_number:
            raise ValueError(_('Either username or phone_number must be set for a superuser'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be staff'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be superuser'))
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_('Superuser must be verified'))

        user = self.create_user(email, password, username=username, mobile_number=mobile_number, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user
