from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)