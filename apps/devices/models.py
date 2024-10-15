from django.db import models

'''
class DeviceType(models.Model):
    name = models.CharField(max_length=100)  # Name of the device type (Mobile, Tablet, Laptop)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)  # Name of the device
    brand = models.CharField(max_length=100)  # Brand of the device (e.g., Samsung, Apple)
    model = models.CharField(max_length=100)  # Model of the device
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='devices')  # Link to DeviceType

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp for last update

    def __str__(self):
        return f'{self.brand} {self.model}'


class DeviceIssue(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='issues')  # Link to Device
    description = models.TextField()  # Description of the issue (e.g., screen cracked, battery issues)

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the issue was reported
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp for when the issue was last updated

    def __str__(self):
        return f'Issue for {self.device}: {self.description}'
'''