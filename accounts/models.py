from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class UserManager(BaseUserManager):

    def create_user(self, email):
        User.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def is_staff(self):
        return self.email == 'hello@rattletat.com'

    @property
    def is_active(self):
        return True
