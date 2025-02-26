from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from .manager import UserManager 


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="job_api_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="job_api_users_permissions",  
        blank=True
    )

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['username']

    objects = UserManager() 

    def __str__(self):
        return self.email

