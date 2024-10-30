from django.shortcuts import render

from apps.users.models import Technician, User

def home(request):
    user_type = None
    if request.user.is_authenticated:
        if isinstance(request.user, Technician):
            user_type = 'technician'
        elif isinstance(request.user, User):
            user_type = 'user'
    
    return render(request, 'home.html', {'user_type': user_type})
