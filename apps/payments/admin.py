from django.contrib import admin
from .models import Payment, PaymentMethod

admin.site.register(Payment)
admin.site.register(PaymentMethod)