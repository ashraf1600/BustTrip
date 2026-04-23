from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bus(models.Model):
    bus_name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    features = models.TextField()
    start_time = models.DateTimeField()
    reach_time = models.DateTimeField()
    no_of_seats = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return  f"{self.bus_name} {self.number} from {self.origin} to {self.destination}"


class Seats(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE , related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} on {self.bus}"
    




class Booking(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seats, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.bus} - Seat {self.seat.seat_number}"