from django.db import models
from apps.users.models import User
from apps.services.models import TechnicianService
from apps.specialties.models import Specialty

class RequestStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
'''
class Device(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.brand} {self.model}'
'''

class Request(models.Model):
    rut_user = models.ForeignKey(User, on_delete=models.CASCADE)
    technician_service = models.ForeignKey(TechnicianService, on_delete=models.CASCADE)
    request_date = models.DateField()
    id_status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    #device = models.ForeignKey(Device, on_delete=models.CASCADE)
    id_specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    customer_comment = models.TextField()
    technician_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
