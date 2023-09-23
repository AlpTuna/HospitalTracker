# myapp/auth_backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomUserModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
