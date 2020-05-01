from django.db import models
# from django.contrib import auth
import uuid

# auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True, default=None)
    identifier = models.TextField(default=None, unique=True, null=True, blank=True, max_length=8)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = models.EmailField()
    identifier = models.CharField(default=None, unique=True, null=True, blank=True, max_length=8)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
