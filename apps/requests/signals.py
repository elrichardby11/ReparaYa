from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def cargar_datos_por_defecto(sender, **kwargs):
    if sender.name == 'apps.requests':
        RequestStatus = apps.get_model('requests', 'RequestStatus')

        rows = [
            {'name': 'Pendiente', 'description': 'Solicitud no tomada por un técnico'},
            {'name': 'En Proceso', 'description': 'Solicitud tomada por un técnico que está en reparación'},
            {'name': 'Completado', 'description': 'Solicitud completada y dispositivo reparado'},
            {'name': 'Cancelado', 'description': 'Solicitud cancelada por algún motivo en especial'},
        ]

        for row in rows:
            RequestStatus.objects.get_or_create(name=row['name'], defaults={'description': row['description']})
