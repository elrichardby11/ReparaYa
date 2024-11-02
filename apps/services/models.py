from django.db import models
from apps.users.models import Technician

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class TechnicianService(models.Model):
    rut_technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    id_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("rut_technician", "id_service"))