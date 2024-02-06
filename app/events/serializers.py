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
        fields = ['id', 'organizer', 'date', 'venue', 'tickets']
        read_only_fields = ['organizer']

    def create(self, validated_data):
        print(validated_data)
        print(self.context.keys())
        print(self.context['request'])
        print(self.context['view'])
        print(self.context['format'])
        user = self.context['request'].user
        # if user.role == 'organizer':
        #     event_organizer = user
        # else:
        #     print(user.role)
        #     print(user.email)
        #     print(user.role)

        #     raise serializers.ValidationError("Current user is not mapped to an event organizer.")
        try:
            event_organizer = EventOrganizer.objects.get(user=user)
        except EventOrganizer.DoesNotExist:
            raise serializers.ValidationError("Current user is not mapped to an event organizer.")


        # Assign the current user as the organizer
        validated_data['organizer'] = event_organizer

        # Create the event
        event = Event.objects.create(**validated_data)

        return event


