from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def cargar_datos_por_defecto(sender, **kwargs):
    if sender.name == 'apps.specialties':
        Specialty = apps.get_model('specialties', 'Specialty')

        rows = [
            {'name': 'Celular', 'description': 'Todo tipo de dispositivos móviles'},
            {'name': 'Tablet', 'description': 'Todo tipo de dispositivos tables'},
            {'name': 'Notebook', 'description': 'Todo tipo de notebook'},
            {'name': 'PC', 'description': 'Todo tipo de pc de escritorios'},
        ]

        for row in rows:
            Specialty.objects.get_or_create(name=row['name'], defaults={'description': row['description']})
