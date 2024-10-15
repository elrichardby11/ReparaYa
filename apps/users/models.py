from django.db import models
from apps.specialties.models import Specialty

class User(models.Model):
    rut = models.CharField(max_length=8, primary_key=True)
    dv = models.CharField(max_length=2)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Technician(models.Model):
    rut = models.CharField(max_length=8, primary_key=True)
    dv = models.CharField(max_length=2)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class TechnicianSpecialty(models.Model):
    rut_technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    id_specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("rut_technician", "id_specialty"))