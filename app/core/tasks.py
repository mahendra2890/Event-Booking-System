"""Task file for celery event tasks"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, message):
    try:
        subject = f'Booking information for {booking_id}'
        message = f'Dear Blej. {message}.\n\nRegards,\nThe Event Team'
        print(subject)
        print(message)
        return f"subbject: {subject}, message: {message}"
    except Exception as e:
        return f" some exception: {str(e)} while attemplting to send: subbject: {subject}, message: {message}"

@shared_task
def send_event_update_notification(event_id, message):
    try:
        subject = f'Booking information for {event_id}'
        message = f'Dear Blej. {message}.\n\nRegards,\nThe Event Team'
        print(subject)
        print(message)
        return f"subbject: {subject}, message: {message}"
    except Exception as e:
        return f" some exception: {str(e)} while attemplting to send: subbject: {subject}, message: {message}"

