from django.contrib import admin
from .models import User, Technician, TechnicianSpecialty

admin.site.register(User)
admin.site.register(Technician)
admin.site.register(TechnicianSpecialty)