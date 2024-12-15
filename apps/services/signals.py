from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import DeviceType, Service

@receiver(post_migrate)
def create_default_services(sender, **kwargs):
    # Lista de tipos de dispositivos y sus servicios correspondientes
    device_types = [
        {
            "name": "Celular",
            "description": "Reparación de teléfonos móviles",
            "services": [
                {"name": "Cambio de pantalla", "description": "Sustitución de pantalla rota"},
                {"name": "Reemplazo de batería", "description": "Sustitución de batería dañada o agotada"},
                {"name": "Reparación de software", "description": "Restauración o instalación del sistema operativo"},
                {"name": "Limpieza de puertos", "description": "Limpieza de puerto de carga o auriculares"},
            ],
        },
        {
            "name": "Tablet",
            "description": "Reparación de tabletas",
            "services": [
                {"name": "Cambio de pantalla", "description": "Sustitución de pantalla rota"},
                {"name": "Reemplazo de batería", "description": "Sustitución de batería dañada o agotada"},
                {"name": "Reparación de conectividad", "description": "Resolución de problemas Wi-Fi o Bluetooth"},
                {"name": "Limpieza interna", "description": "Limpieza de componentes internos"},
            ],
        },
        {
            "name": "Computadora",
            "description": "Reparación de computadoras de escritorio",
            "services": [
                {"name": "Reparación de hardware", "description": "Sustitución de piezas dañadas (RAM, disco duro, etc.)"},
                {"name": "Limpieza de ventiladores", "description": "Limpieza de ventiladores y disipadores de calor"},
                {"name": "Formateo y reinstalación", "description": "Formateo del disco duro y reinstalación del sistema operativo"},
                {"name": "Actualización de hardware", "description": "Mejoras de hardware (SSD, GPU, etc.)"},
            ],
        },
        {
            "name": "PC",
            "description": "Reparación de PCs portátiles",
            "services": [
                {"name": "Cambio de pantalla", "description": "Reemplazo de pantalla rota o dañada"},
                {"name": "Reparación del teclado", "description": "Sustitución de teclas o teclado completo"},
                {"name": "Reemplazo de batería", "description": "Sustitución de batería agotada"},
                {"name": "Reparación de bisagras", "description": "Ajuste o reemplazo de bisagras dañadas"},
            ],
        },
    ]

    # Iteramos sobre cada tipo de dispositivo
    for device_type_data in device_types:
        # Crear o recuperar el tipo de dispositivo
        device_type, created = DeviceType.objects.get_or_create(
            name=device_type_data["name"],
            defaults={"description": device_type_data["description"]}
        )

        # Crear los servicios asociados al tipo de dispositivo
        for service_data in device_type_data["services"]:
            Service.objects.get_or_create(
                name=service_data["name"],
                description=service_data["description"],
                device_type=device_type
            )
