"""Test event APIs"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import EventOrganizer, Customer, Event, Ticket


EVENT_CREATE_URL = reverse('event:event-create')
EVENT_LIST_URL = reverse('event:event-list')
MY_EVENTS_URL = reverse('event:event-list-myevents')

# EVENT_RETRIEVE_BY_ID_URL = reverse('event:event-retrieve-by-id', kwargs={'pk': 1})
# EVENT_UPDATE_URL = reverse('event:event-update', kwargs={'pk': 1})
# TICKET_LIST_URL = reverse('event:ticket-list', kwargs={'event_id': 1})
# TICKET_CREATE_URL = reverse('event:ticket-create', kwargs={'event_id': 1})
# TICKET_UPDATE_URL = reverse('event:ticket-update', kwargs={'event_id': 1, 'pk': 2})


class EventAPITests(TestCase):
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

    def test_create_event_customer_fails(self):
        """Test customer can't create event"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'date': '2024-02-05',
            'venue': 'Test Venue',
        }

        response = self.client.post(EVENT_CREATE_URL, payload)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_event_default_input(self):
        """Test event organizer can create event with default data"""
        self.client.force_authenticate(user=self.orguser)
        payload = {}
        response = self.client.post(EVENT_CREATE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_event_successful(self):
        """Test event organizer can create event"""
        self.client.force_authenticate(user=self.orguser)
        payload = {
            'date': '2024-02-06T21:37:10.409580Z',
            'venue': 'Test Venue',
        }

        response = self.client.post(EVENT_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get(id=response.data['id']).organizer, self.organizer)

    def test_create_event_unauthorized(self):
        """Test unauthorized user can't create event"""
        payload = {
            'date': '2024-02-06T21:37:10.409580Z',
            'venue': 'Test Venue',
        }

        response = self.client.post(EVENT_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Event.objects.count(), 0)

    def test_create_event_invalid_data(self):
        """Test event creation with invalid data"""
        self.client.force_authenticate(user=self.orguser)
        payload = {
            'date': 'Invalid Date',  # Invalid date format
            'venue': 'Test Venue',
        }

        response = self.client.post(EVENT_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)

    def test_list_events(self):
        """Test retrieving list of events"""
        Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)
        response = self.client.get(EVENT_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_create_event_successful(self):
        """Test event organizer can create event"""
        self.client.force_authenticate(user=self.orguser)
        payload = {
            'date': '2024-02-06T21:37:10.409580Z',
            'venue': 'Test Venue',
        }

        response = self.client.post(EVENT_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get(id=response.data['id']).organizer, self.organizer)


    def test_list_my_events_successful(self):
        """Test organizer can list their own events"""
        Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)
        self.client.force_authenticate(user=self.orguser)

        response = self.client.get(MY_EVENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_my_events_unauthorized(self):
        """Test unauthorized user can't list events"""
        response = self.client.get(MY_EVENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_event_by_id_successful(self):
        """Test retrieving event by ID"""
        event = Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)

        response = self.client.get(reverse('event:event-retrieve-by-id', kwargs={'pk': event.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], event.id)

    def test_update_event_successful(self):
        """Test updating event"""
        event = Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)
        self.client.force_authenticate(user=self.orguser)
        updated_data = {'date': '2025-02-06T21:37:10.409580Z', 'venue': 'Updated Venue'}

        response = self.client.patch(reverse('event:event-update', kwargs={'pk': event.id}), updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.date.isoformat(), '2025-02-06T21:37:10.409580+00:00')
        self.assertEqual(event.venue, 'Updated Venue')

    def test_list_tickets_successful(self):
        """Test listing tickets for an event"""
        event = Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)
        Ticket.objects.create(event=event, ticket_type='General', price=10, availability=100)

        response = self.client.get(reverse('event:ticket-list', kwargs={'event_id': event.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_ticket_successful(self):
        """Test creating a ticket for an event"""
        self.client.force_authenticate(user=self.orguser)
        event = Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)
        payload = {'ticket_type': 'General', 'price': 10, 'availability': 100}

        response = self.client.post(reverse('event:ticket-create', kwargs={'event_id': event.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ticket_successful(self):
        """Test updating a ticket for an event"""
        self.client.force_authenticate(user=self.orguser)
        event = Event.objects.create(date='2024-02-06T21:37:10.409580Z', venue='Test Venue', organizer=self.organizer)
        ticket = Ticket.objects.create(event=event, ticket_type='General', price=10, availability=100)
        updated_data = {'ticket_type': 'VIP', 'price': 20, 'availability': 50}

        response = self.client.patch(reverse('event:ticket-update', kwargs={'event_id': event.id, 'pk': ticket.id}), updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.ticket_type, 'VIP')
        self.assertEqual(ticket.price, 20)
        self.assertEqual(ticket.availability, 50)
