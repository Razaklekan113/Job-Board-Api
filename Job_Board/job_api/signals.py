from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, EmployerProfile, ApplicantProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'employer':
            EmployerProfile.objects.create(user=instance)
        elif instance.role == 'applicant':
            ApplicantProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
