from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.location}"
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room')
    room_type = models.CharField(max_length=100)
    beds = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.IntegerField(default=1)
    amenities = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"
    
class Booking(models.Model):
    STATUS_CHOCIES = (('Booked', 'Booked'), ('Cancelled', 'Cancelled'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOCIES, default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room} ({self.check_in} -> {self.check_out})"