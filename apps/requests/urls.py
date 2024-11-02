from django.urls import path
from . import views

urlpatterns = [
    # User
    path("", views.requests, name="user_requests"),
    path("request_detail/<int:id>", views.requests, name="user_request_detail"),
    path("add/", views.add_request, name="user_add_request"),
    # Technician
    path("pendings", views.tech_requests, name="tech_requests"),
    path("pendings/request_detail/<int:id>", views.tech_requests, name="tech_request_detail"),
]
