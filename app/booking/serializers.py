"""Serializers for Booking API view"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.models import EventOrganizer, Customer, Booking, Event, Ticket


class BookingSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = Booking
        fields = ['quantity']



    def create(self, validated_data):
        # Extract event_id and ticket_id from the context
        event_id = self.context['view'].kwargs['event_id']
        ticket_id = self.context['view'].kwargs['ticket_id']

        # Get event and ticket objects
        event = Event.objects.get(pk=event_id)
        ticket = Ticket.objects.get(pk=ticket_id)

        # Check if the ticket is available
        if ticket.availability < validated_data['quantity']:
            raise serializers.ValidationError("Requested quantity exceeds available tickets.")


        # Set customer based on authenticated user
        customer = self.context['request'].user.customer

        # Create booking
        booking = Booking.objects.create(event=event, ticket=ticket, customer=customer, quantity=validated_data['quantity'])

        return booking

class BookingUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = Booking
        fields = ['quantity']

    def validate(self, data):
        # Check if the quantity is provided
        quantity = data.get('quantity')
        if not quantity:
            raise serializers.ValidationError("Quantity is required.")

        return data

    def update(self, instance, validated_data):
        # Retrieve the previous quantity
        previous_quantity = instance.quantity
        print(previous_quantity)
        # Update the quantity of the booking
        instance.quantity = validated_data.get('quantity', instance.quantity)
        print(instance.quantity)
        instance.save()

        # Calculate the difference in quantity
        # quantity_difference = instance.quantity - previous_quantity

        # Update the ticket availability accordingly
        # instance.ticket.availability -= quantity_difference
        # instance.ticket.save()
        return instance

class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'