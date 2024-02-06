# views.py

from rest_framework import generics, permissions
from core.models import Event, EventOrganizer, Ticket
from events.serializers import EventSerializer, TicketSerializer, CreateTicketSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import authentication

# class EventApiCreateSerializer(serializers.Serializer):
#     id = serializers.ReadOnlyField()  # Make id read-only
#     date = serializers.DateField(required=True, format="%Y-%m-%d")
#     venue = serializers.CharField(default="TBD")

#     class Meta:
#         # You can define metadata options here if needed
#         pass

#     def validate(self, data):
#         # Validate that the user creating the event is an EventOrganizer
#         validate_user_is_event_organizer(self.context['request'].user)
#         return data

#     def create(self, validated_data):
#         # Get the current user from the context
#         user = self.context['request'].user

#         # Create a new event with the current user as the organizer
#         event = Event.objects.create(
#             organizer=user,
#             date=validated_data['date'],
#             venue=validated_data['venue']
#         )

#         return event

#     def to_representation(self, instance):
#         # Include id field in serialized data
#         data = super().to_representation(instance)
#         data['id'] = instance.id
#         return data

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



# class MyEventRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#     serializer_class = EventSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     allowed_methods = ['GET', 'PATCH']

#     def get_queryset(self):
#         user = self.request.user
#         try:
#             event_organizer = EventOrganizer.objects.get(user=user)
#             return Event.objects.filter(organizer=event_organizer)
#         except EventOrganizer.DoesNotExist:
#             return Event.objects.none()


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
    serializer_class = CreateTicketSerializer  # Using the same serializer as create view
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['PATCH']
