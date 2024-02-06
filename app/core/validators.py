# validators.py

from rest_framework.exceptions import ValidationError
from .models import EventOrganizer

def validate_user_is_event_organizer(user):
    try:
        # Check if the user has a corresponding EventOrganizer
        event_organizer = EventOrganizer.objects.get(user=user)
    except EventOrganizer.DoesNotExist:
        raise ValidationError("User is not allowed to create an event.")
