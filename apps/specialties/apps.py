from django.apps import AppConfig


class SpecialtiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.specialties"
    
    def ready(self):
        import apps.specialties.signals