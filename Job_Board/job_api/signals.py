from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, EmployerProfile, ApplicantProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'employer':
            EmployerProfile.objects.create(user=instance)
        elif instance.role == 'applicant':
            ApplicantProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Dynamically save the correct profile
    if instance.role == 'employer' and hasattr(instance, 'employer_profile'):
        instance.employer_profile.save()
    elif instance.role == 'applicant' and hasattr(instance, 'applicant_profile'):
        instance.applicant_profile.save()
