# urls.py

from django.urls import path
from events.views import *

app_name = 'event'

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='create'),
    path('', EventListView.as_view(), name='list'),
    path('myevents/', MyEventListView.as_view(), name='listmyevents'),
]
