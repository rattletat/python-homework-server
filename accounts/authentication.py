from accounts.models import User


class PasswordlessAuthenticationBackend(object):

    def authenticate(self, request, uid):
        try:
            return User.objects.get(uid=uid)
        except User.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
