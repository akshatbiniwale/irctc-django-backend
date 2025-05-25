from django.db import models
from trains.models import Train
from user.models import User

# Create your models here.

class Status(models.TextChoices):
    BOOKED = 'booked', 'Booked'
    CANCELLED = 'cancelled', 'Cancelled'

class Booking(models.Model):
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BOOKED
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)