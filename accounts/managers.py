'''
Since we are using email+password for authentication, 
insted of Djangos AbstractUser which allows for username + password for authentication 
we need to define a custom Manager.
'''


from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Custom manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # For admin role, 'is_stuff = True' & 'default role = doctor'
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "doctor")
        return self.create_user(email, password, **extra_fields)
