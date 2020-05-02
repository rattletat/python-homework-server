import uuid
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.core.validators import (
    EmailValidator,
    MinValueValidator,
    MaxValueValidator,
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
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator(code="invalid")])
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
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.identifier:
            return f"{self.email} ({self.identifier})"
        else:
            return f"{self.email} (extern)"

    def get_short_name(self):
        return self.email
