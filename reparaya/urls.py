from django.contrib import admin
from django.urls import path

from reparaya import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("register/user", views.register_user, name="register_user"),
    path("register/tech", views.register_tech, name="register_tech"),
]
