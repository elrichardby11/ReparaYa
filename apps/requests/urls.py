from django.urls import path
from . import views

urlpatterns = [
    # User
    path("", views.requests, name="user_requests"),
    path("request_detail/<int:id>", views.requests, name="user_request_detail"),
    path("add/", views.add_request, name="user_add_request"),
    path("technicians", views.technicians, name="technicians"),
    path("technicians/<int:id>", views.technicians, name="technicians_detail"),
    # Technician
    path("pendings", views.tech_requests, name="tech_requests"),
    path("pendings/request_detail/<int:id>", views.tech_requests, name="tech_request_detail"),
    path('<int:request_id>/quotation/create/', views.create_quotation, name='create_quotation'),

]
