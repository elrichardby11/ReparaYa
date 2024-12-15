from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from reparaya import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("users/", include('apps.users.urls')),
    path("request/", include('apps.requests.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
