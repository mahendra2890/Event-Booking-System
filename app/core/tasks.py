"""Task file for celery event tasks"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from core.models import Booking, Event

@shared_task
def send_booking_confirmation_email(booking_id):
    try:
        subject = f'Booking Confirmation for BLAH'
        message = f'Dear Blej. Your booking details:\n\nEvent:sdvgdour records.\n\nRegards,\nThe Event Team'
        sender = settings.EMAIL_HOST_USER
        recipient = ['cmahendra9999@gmail.com']
        send_mail(subject, message, sender, recipient)
        return f"Confirmation email sent for booking ID: {booking_id}"
    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} does not exist."

@shared_task
def send_event_update_notification(event_id):
    try:
        subject = f'Booking Confirmation for BLAH'
        message = f'Dear Blej. Your booking details:\n\nEvent:sdvgdour records.\n\nRegards,\nThe Event Team'
        sender = settings.EMAIL_HOST_USER
        recipient = ['cmahendra9999@gmail.com']
        send_mail(subject, message, sender, recipient)
        return f"Confirmation email sent for booking ID: {event_id}"
    except Booking.DoesNotExist:
        return f"Booking with ID {event_id} does not exist."
