"""
Event Views
"""

from rest_framework import generics, permissions
from core.models import Booking, Event, Customer, Ticket
from events.serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import authentication

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_context(self):

        print(self.request.user.email)
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class MyEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            event_organizer = EventOrganizer.objects.get(user=user)
            return Event.objects.filter(organizer=event_organizer)
        except EventOrganizer.DoesNotExist:
            return Event.objects.none()


class MyEventRetrieveView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        try:
            return Event.objects
        except Exception as e:
            raise e


class MyEventUpdateView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['PATCH']

    def get_queryset(self):
        user = self.request.user
        try:
            event_organizer = EventOrganizer.objects.get(user=user)
            return Event.objects.filter(organizer=event_organizer)
        except EventOrganizer.DoesNotExist:
            return Event.objects.none()


class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        return Ticket.objects.filter(event_id=event_id)

class TicketCreateView(generics.CreateAPIView):
    serializer_class = CreateTicketSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id)
        serializer.save(event=event)

class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['PATCH']
