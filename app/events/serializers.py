# serializers.py

from rest_framework import serializers
from core.models import Event, Ticket, EventOrganizer
from core.validators import validate_user_is_event_organizer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'ticket_type', 'price', 'availability']

class EventSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'organizer', 'date', 'venue', 'tickets', 'description', 'title']
        read_only_fields = ['organizer', 'id']

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            event_organizer = EventOrganizer.objects.get(user=user)
        except EventOrganizer.DoesNotExist:
            raise serializers.ValidationError("Current user is not mapped to an event organizer.")


        # Assign the current user as the organizer
        validated_data['organizer'] = event_organizer

        # Create the event
        event = Event.objects.create(**validated_data)

        return event


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'ticket_type', 'price', 'availability']
        read_only_fields = ['id', 'event']  # Ensure event cannot be changed when updating

class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'price', 'availability']
