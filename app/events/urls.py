# urls.py

from django.urls import path
from events.views import *

app_name = 'event'

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('', EventListView.as_view(), name='event-list'),
    path('myevents/', MyEventListView.as_view(), name='event-list-myevents'),
    path('<int:pk>/', MyEventRetrieveView.as_view(), name='event-retrieve-by-id'),
    path('<int:pk>/update/', MyEventUpdateView.as_view(), name='event-update'),
    path('<int:event_id>/tickets/', TicketListView.as_view(), name='ticket-list'),
    path('<int:event_id>/tickets/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:event_id>/tickets/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
]