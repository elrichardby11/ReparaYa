from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("register/user/", views.register_user, name="register_user"),
    path("register/tech/", views.register_tech, name="register_tech"),
    path("logout/", views.logout, name="logout"),
]
