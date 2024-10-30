from django.contrib.auth.backends import ModelBackend
from .models import User, Technician

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        try:
            technician = Technician.objects.get(email=email)
            if technician.check_password(password):
                return technician
        except Technician.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            try:
                return Technician.objects.get(pk=user_id)
            except Technician.DoesNotExist:
                return None
