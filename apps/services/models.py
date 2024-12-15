from django.db import models

class DeviceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name
