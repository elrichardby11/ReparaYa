# apps/users/decorators.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import Technician, User

def technician_required(view_func):
    """Decorator that allows only technicians to access the view."""
    @wraps(view_func)
    @login_required  # Asegura que el usuario esté autenticado
    def _wrapped_view(request, *args, **kwargs):
        if isinstance(request.user, Technician):
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home')) 
    return _wrapped_view

def user_required(view_func):
    """Decorator that allows only regular users to access the view."""
    @wraps(view_func)
    @login_required  # Asegura que el usuario esté autenticado
    def _wrapped_view(request, *args, **kwargs):
        if isinstance(request.user, User):
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home'))
    return _wrapped_view
