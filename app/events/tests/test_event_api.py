"""Test event APIs"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import EventOrganizer, Customer, Event

CREATE_EVENT_URL = reverse('event:create')


class EventListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass',
            name='Test User',
            role='customer'
        )
        self.customer = Customer.objects.create(user=self.user, customer_specific_field='thiscamefromtest')

        self.orguser = get_user_model().objects.create_user(
            email='organizer@example.com',
            password='organizerpass',
            name='Test Organizer',
            role='organizer'
        )
        self.organizer = EventOrganizer.objects.create(user=self.orguser)

        self.client.force_authenticate(user=self.orguser)

    def test_create_event_existing_organizer(self):
        """Test event organizer can create event"""

        payload = {
            'date': '2024-02-06T21:37:10.409580Z',
            'venue': 'Test Venue',
        }

        response = self.client.post(CREATE_EVENT_URL, payload)

        # Assert that 'id' is present in the event data
        self.assertIn('id', response.data)
        event_id = response.data['id']

        # Retrieve the event from the database using the event ID
        created_event = Event.objects.get(id=event_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventOrganizer.objects.count(), 1)
        self.assertEqual(created_event.organizer.id, self.organizer.id)

    def test_create_event_customer_fails(self):
        """Test customer can't create event"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'date': '2024-02-05',
            'venue': 'Test Venue',
        }

        response = self.client.post(CREATE_EVENT_URL, payload)
        print(response.data)
        print(response.status_code)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_event_default_input(self):
        """Test event organizer can create event with default data"""
        payload = {}
        response = self.client.post(CREATE_EVENT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

