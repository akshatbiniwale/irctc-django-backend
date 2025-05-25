from django.db import models
from user.models import User

# Create your models here.

class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    totalSeats = models.IntegerField()
    availableSeats = models.IntegerField()
    adminId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)