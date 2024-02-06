"""Signals implemented for updates"""
"""Not comprehensive, hence removed the existing and commenting the basic logic and structure, just wanted to show that this is also an option"""
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from core.models import User, EventOrganizer, Customer, Event, Ticket, Booking

# @receiver(post_save, sender=User)
# def update_user_related_models(sender, instance, **kwargs):
#     pass

# @receiver(post_delete, sender=Booking)
# def update_ticket_availability_on_delete(sender, instance, **kwargs):
#     pass