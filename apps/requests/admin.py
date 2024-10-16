from django.contrib import admin
from .models import Request, RequestStatus

admin.site.register(Request)
admin.site.register(RequestStatus)