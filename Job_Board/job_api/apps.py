from django.apps import AppConfig


class JobApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_api'

def ready(self):
    import job_api.signals 
