from django.urls import path
from . import views

urlpatterns = [
    path("", views.requests, name="requests"),
    path("request_detail/<int:id>", views.requests, name="request_detail"),
    path("add/", views.add_request, name="add_request")
]
