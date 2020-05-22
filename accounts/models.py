import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import (
    EmailValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

IDENTIFER_MIN_NUMBER = 1000
IDENTIFER_MAX_NUMBER = 99999999


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        primary_key=True, unique=True, validators=[EmailValidator(code="invalid")]
    )
    email_verified = models.BooleanField(default=False)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=20, default="", editable=False)
    identifier = models.IntegerField(
        default=None,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(IDENTIFER_MIN_NUMBER),
            MaxValueValidator(IDENTIFER_MAX_NUMBER),
        ],
    )
    USERNAME_FIELD = "email"
    objects = MyUserManager()
    is_staff = models.BooleanField("staff status", default=False,)

    def __str__(self):
        if self.identifier:
            return f"{self.email} (TUM Student: {self.identifier})"
        else:
            return f"{self.email} (TUM extern)"
