"""URL mappings for Booking APIs"""
from django.urls import path

from booking.views import *

app_name = 'booking'

urlpatterns = [
    path('<int:event_id>/<int:ticket_id>/book/', BookingCreateView.as_view(), name='booking-book'),
    path('<int:pk>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('<int:pk>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
    path('mybookings/', BookingListView.as_view(), name='booking-list'),
    path('myeventbookings/<int:event_id>/', EventBookingListView.as_view(), name='event-bookings'),
]