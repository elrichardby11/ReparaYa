from django.db import models
from apps.users.models import User
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
    request_date = models.DateField()
    id_status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE, default=1)
    #device = models.ForeignKey(Device, on_delete=models.CASCADE)
    id_specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Quotation(models.Model):
    request = models.ForeignKey('requests.Request', on_delete=models.CASCADE, related_name='quotations')
    technician = models.ForeignKey('users.Technician', on_delete=models.CASCADE, related_name='quotations')
    estimated_cost = models.IntegerField()
    estimated_duration = models.IntegerField()
    location = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("request", "technician"))

class QuotationService(models.Model):
    quotation = models.ForeignKey('requests.Quotation', on_delete=models.CASCADE, related_name='quotation_services')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='quotation_services')
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("quotation", "service"))