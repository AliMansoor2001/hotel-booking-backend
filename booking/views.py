from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from datetime import date

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.select_related('hotel').all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    # list available rooms by query params: hotel, check_in, check_out
    def list(self, request, *args, **kwargs):
        hotel_id = request.GET.get('hotel')
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')

        qs = self.queryset
        if hotel_id:
            qs = qs.filter(hotel_id=hotel_id)

        if check_in and check_out:
            from django.utils.dateparse import parse_date
            ci = parse_date(check_in)
            co = parse_date(check_out)
            # Find rooms where number of bookings overlapping < total_rooms
            available = []
            for room in qs:
                overlapping = Booking.objects.filter(
                    room=room
                ).filter(
                    Q(check_in__lt=co) & Q(check_out__gt=ci)
                ).count()
                if overlapping < room.total_rooms:
                    available.append(room)
            serializer = self.get_serializer(available, many=True)
            return Response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        room = serializer.validated_data['room']

        # basic overlap check for available rooms
        overlapping = Booking.objects.filter(room=room).filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        ).count()
        if overlapping >= room.total_rooms:
            raise serializers.ValidationError("No rooms available for selected dates.")
        # compute nights
        nights = (check_out - check_in).days
        total_price = room.price * nights
        serializer.save(user=user, total_price=total_price)
