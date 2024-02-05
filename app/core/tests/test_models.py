"""
Test custom django models
"""
from decimal import Decimal
from datetime import datetime
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import EventOrganizer, Customer, Event, Ticket, Booking


class ModelTests(TestCase):
    """Test Models"""

    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user('org@example.com', 'pass123', role='organizer')
        self.organizer = EventOrganizer.objects.create(user=self.organizer_user)

        self.customer_user = get_user_model().objects.create_user('customer@example.com', 'pass123', role='customer')
        self.customer = Customer.objects.create(user=self.customer_user)

        self.event = Event.objects.create(organizer=self.organizer, date=datetime(2024, 2, 5), venue='Some Test Venue')

        self.ticket = Ticket.objects.create(event=self.event, ticket_type='VIP', price=Decimal('100.00'), availability=1000)


    def test_create_user_with_email_successfully(self):
        """Test creating a user with an email is successful """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TeSt3@example.com', 'TeSt3@example.com'],
        ]

        for email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'pass123')
            self.assertEqual(user.email, normalized_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_create_superuser(self):
        """Test creating a superuser"""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_event_organizer(self):
        """Test creating an Event Organizer"""
        user = get_user_model().objects.create_user(email='testuser@example.com', password='pass123', role='organizer')
        organizer = EventOrganizer.objects.create(user=user)

        self.assertEqual(organizer.user, user)

    def test_event_organizer_model_role_enforcement(self):
        """Test EventOrganizer model enforces 'organizer' role for associated user"""
        user = get_user_model().objects.create_user('testuser@example.com', 'pass123', role='customer')
        with self.assertRaises(ValidationError):
            EventOrganizer.objects.create(user=user)

    def test_create_customer(self):
        """Test creating a Customer"""
        user = get_user_model().objects.create_user('testuser@example.com', 'pass123', role='customer')
        customer = Customer.objects.create(user=user)

        self.assertEqual(customer.user, user)

    def test_customer_model_role_enforcement(self):
        """Test Customer model enforces 'customer' role for associated user"""
        user = get_user_model().objects.create_user('testuser@example.com', 'pass123', role='organizer')
        with self.assertRaises(ValidationError):
            Customer.objects.create(user=user)

    def test_create_event(self):
        """Test creating an Event"""
        event = Event.objects.create(organizer=self.organizer, date=datetime(2024, 2, 5), venue='Venue')
        self.assertEqual(event.organizer, self.organizer)
        self.assertEqual(event.date.strftime('%Y-%m-%d'), '2024-02-05')
        self.assertEqual(event.venue, 'Venue')

    def test_create_event_with_non_organizer_raises_error(self):
        """Test creating an Event with a non-organizer raises ValidationError"""
        with self.assertRaises(ValueError):
            Event.objects.create(organizer=self.customer, date=datetime(2024, 2, 5), venue='Test Venue')


    def test_create_ticket(self):
        """Test creating a Ticket"""
        ticket = Ticket.objects.create(event=self.event, ticket_type='VIP', price=Decimal('100.00'), availability=100)

        self.assertEqual(ticket.event, self.event)
        self.assertEqual(ticket.ticket_type, 'VIP')
        self.assertEqual(ticket.price, Decimal('100.00'))
        self.assertEqual(ticket.availability, 100)

    def test_create_ticket_with_non_organizer_raises_error(self):
        """Test creating a Ticket with a non-organizer raises ValidationError"""

        with self.assertRaises(ValueError):
            Event.objects.create(organizer=self.customer, date=datetime(2024, 2, 5), venue='Test Venue')


    def test_create_booking(self):
        """Test creating a Booking"""
        booking = Booking.objects.create(customer=self.customer, event=self.event, ticket=self.ticket, quantity=99)

        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.ticket, self.ticket)
        self.assertEqual(booking.quantity, 99)

    def test_create_booking_with_non_customer_raises_error(self):
        """Test creating an Event with a non-customer raises ValidationError"""

        with self.assertRaises(ValueError):
            Booking.objects.create(customer=self.organizer, event=self.event, ticket=self.ticket, quantity=99)


    def test_create_booking_update_ticket_availability(self):
        """Test creating a Booking updates Ticket availability"""
        ticket = Ticket.objects.create(event=self.event, ticket_type='VIP', price=Decimal('100.00'), availability=100)

        booking = Booking.objects.create(customer=self.customer, event=self.event, ticket=ticket, quantity=2)

        # Check if ticket availability is updated
        updated_ticket = Ticket.objects.get(pk=ticket.pk)
        self.assertEqual(updated_ticket.availability, 98)

    def test_create_booking_exceeding_ticket_availability(self):
        """Test creating a Booking exceeding Ticket availability raises ValidationError"""
        with self.assertRaises(ValidationError):
            Booking.objects.create(customer=self.customer, event=self.event, ticket=self.ticket, quantity=100001)


    def test_booking_model_role_enforcement(self):
        """Test Booking model enforces 'customer' role for associated user"""

        with self.assertRaises(ValueError):
            Booking.objects.create(customer=self.organizer, event=self.event, ticket=self.ticket, quantity=2)

