from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
import uuid
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, related_name="job_api_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="job_api_users_permissions", blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class EmployerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    company_size = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Employer"


class ApplicantProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="applicant_profile")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Applicant"
    

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("full_time", "Full-Time"),
        ("part_time", "Part-Time"),
        ("remote", "Remote"),
        ("contract", "Contract"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    location = models.CharField(max_length=255)
    salary = models.PositiveIntegerField(null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

