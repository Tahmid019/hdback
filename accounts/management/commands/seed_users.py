"""
Create test users for each role (doctor, technician, patient).

Use by:
    python manage.py seed_users
"""

from django.core.management.base import BaseCommand
from accounts.models import User


SEED_USERS = [
    {"email": "doctor@test.com",     "name": "Dr. Aris Thorne",   "role": "doctor",     "password": "test1234"},
    {"email": "tech@test.com",       "name": "Tech. Maya Singh",  "role": "technician", "password": "test1234"},
    {"email": "patient@test.com",    "name": "James O'Brien",     "role": "patient",    "password": "test1234"},
]


class Command(BaseCommand):
    help = "Create test users for each role (skips existing)"

    def handle(self, *args, **options):
        for data in SEED_USERS:
            user, created = User.objects.get_or_create(
                email=data["email"],     # it searches by this (the non default)
                defaults={"name": data["name"], "role": data["role"]},
            )
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Created {data['role']}: {data['email']} (password: {data['password']})"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Already exists: {data['email']}"
                ))
