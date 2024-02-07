"""
Booking Views
"""

from rest_framework import generics
from core.models import Booking, Ticket
from booking.serializers import *
from rest_framework import authentication, permissions
from django.db import transaction


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set customer based on authenticated user
        customer = self.request.user.customer
        event_id = self.kwargs['event_id']
        ticket_id = self.kwargs['ticket_id']

        try:
            # Create booking
            serializer.save(customer=customer, event_id=event_id, ticket_id=ticket_id)
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("Ticket not found.")

class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Filter bookings associated with the authenticated customer
        user = self.request.user
        if user.role == 'customer':
            return Booking.objects.filter(customer__user=user)
        else:
            # Event organizers or other roles may have different permissions
            return Booking.objects.none()

class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Filter bookings associated with the authenticated customer
        user = self.request.user
        if user.role == 'customer':
            return Booking.objects.filter(customer__user=user)
        else:
            # Event organizers or other roles may have different permissions
            return Booking.objects.none()



class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter bookings based on authenticated user
        return Booking.objects.filter(customer=self.request.user.customer)


class EventBookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        user = self.request.user
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Booking.objects.none()

        # Check if the event is created by the Event Organizer corresponding to the user
        if user.is_authenticated and user.role == 'organizer' and event.organizer.user == user:
            # Return bookings for the event
            return Booking.objects.filter(event=event)

        return Booking.objects.none()

