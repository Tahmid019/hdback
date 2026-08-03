from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("doctor", "Doctor"),
        ("technician", "Technician"),
        ("patient", "Patient"),
    ]

    # Supabase Auth user id (JWT "sub")
    supabase_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="patient",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.role})"