from django.contrib import admin
from django.urls import include, path

from reparaya import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("users/", include('apps.users.urls')),
    path("request/", include('apps.requests.urls')),
]
