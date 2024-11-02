from apps.users.models import Technician, User

def user_type(request):
    user_type = None
    if request.user.is_authenticated:
        if isinstance(request.user, Technician):
            user_type = 'technician'
        elif isinstance(request.user, User):
            user_type = 'user'
    
    return {'user_type': user_type}
