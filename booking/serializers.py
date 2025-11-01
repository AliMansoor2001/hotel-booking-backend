from rest_framework import serializers
from .models import Hotel, Room, Booking
from django.contrib.auth.models import User

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
