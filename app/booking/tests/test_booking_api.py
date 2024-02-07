"""Tests for booking APIs"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import User, Customer, Event, Ticket, EventOrganizer, Booking
from rest_framework.authtoken.models import Token

class BookingTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        """Create Event Organizer"""
        self.organizer_user = User.objects.create_user(email='organizer@example.com', password='password', role='organizer')
        self.organizer = EventOrganizer.objects.create(user=self.organizer_user)

        # Create Event
        self.event = Event.objects.create(organizer=self.organizer, title='Test Event', venue='Test Venue')

        # Create Ticket
        self.ticket = Ticket.objects.create(event=self.event, ticket_type='Test Ticket', price=10.00, availability=10)

        # Create Customers
        self.customer1_user = User.objects.create_user(email='customer1@example.com', password='password', role='customer')
        self.customer1 = Customer.objects.create(user=self.customer1_user)
        self.customer1_token = Token.objects.create(user=self.customer1_user)  # Create Token for customer 1


        self.customer2_user = User.objects.create_user(email='customer2@example.com', password='password', role='customer')
        self.customer2 = Customer.objects.create(user=self.customer2_user)
        self.customer2_token = Token.objects.create(user=self.customer2_user)  # Create Token for customer 2

    def assertTicketAvailability(self, ticket, expected_availability):
        updated_ticket = Ticket.objects.get(pk=ticket.pk)
        self.assertEqual(updated_ticket.availability, expected_availability)

    def test_booking_tickets_concurrently(self):
        #"""Concurrently book tickets for the same event """
        booking_data1 = {'quantity': 3}
        booking_data2 = {'quantity': 4}


        url = reverse('booking:booking-book', kwargs={'event_id': self.event.pk, 'ticket_id': self.ticket.pk})

        # Perform concurrent booking requests
        response1 = self.client.post(url, booking_data1, HTTP_AUTHORIZATION='Token ' + self.customer2_token.key)
        response2 = self.client.post(url, booking_data2, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)

        # Check responses
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)

        # Check ticket availability after bookings
        updated_ticket = Ticket.objects.get(pk=self.ticket.pk)
        self.assertTicketAvailability(self.ticket, 3)  # Remaining tickets after customer 1 booking

    def test_booking_tickets_invalid_quantity(self):
        """Attempt to book tickets with an invalid quantity"""
        invalid_booking_data = {'quantity': -1}  # Invalid quantity

        # Generate the URL for booking tickets
        url = reverse('booking:booking-book', kwargs={'event_id': self.event.pk, 'ticket_id': self.ticket.pk})

        # Perform booking request with invalid quantity
        response = self.client.post(url, invalid_booking_data, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)

        # Check response
        self.assertEqual(response.status_code, 400)  # Bad request due to invalid quantity

        # Check ticket availability remains unchanged
        self.assertTicketAvailability(self.ticket, 10)

    def test_booking_tickets_insufficient_availability(self):
        """ Attempt to book tickets with quantity exceeding availability"""
        booking_data = {'quantity': 20}  # Quantity exceeds availability

        # Generate the URL for booking tickets
        url = reverse('booking:booking-book', kwargs={'event_id': self.event.pk, 'ticket_id': self.ticket.pk})

        # Perform booking request with quantity exceeding availability
        response = self.client.post(url, booking_data, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)

        # Check response
        self.assertEqual(response.status_code, 400)  # Bad request due to insufficient availability

        # Check ticket availability remains unchanged
        self.assertTicketAvailability(self.ticket, 10)

    def test_cancel_booking(self):
        """ Create a booking """
        booking = Booking.objects.create(customer=self.customer1, event=self.event, ticket=self.ticket, quantity=2)

        # Generate the URL for canceling the booking
        url = reverse('booking:booking-delete', kwargs={'pk': booking.pk})

        # Perform cancel booking request
        response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)

        # Check response
        self.assertEqual(response.status_code, 204)  # Successful cancellation
        self.assertFalse(Booking.objects.filter(pk=booking.pk).exists())  # Booking should no longer exist

        # Check ticket availability is restored
        self.assertTicketAvailability(self.ticket, 10)

    def test_cancel_booking_unauthorized(self):
        """ Create a booking """
        booking = Booking.objects.create(customer=self.customer1, event=self.event, ticket=self.ticket, quantity=2)

        # Generate the URL for canceling the booking
        url = reverse('booking:booking-delete', kwargs={'pk': booking.pk})

        # Perform cancel booking request with unauthorized user
        response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + self.customer2_token.key)

        # Check response
        self.assertEqual(response.status_code, 404)  # No content for this request for this user
        self.assertTicketAvailability(self.ticket, 8)

        response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)
        self.assertEqual(response.status_code, 204)  # delete for this user
        self.assertTicketAvailability(self.ticket, 10)


        # Check ticket availability remains unchanged

    def test_cancel_nonexistent_booking(self):
        """Attempt to cancel a nonexistent booking """
        nonexistent_booking_id = 9999  # Nonexistent booking ID

        # Generate the URL for canceling the booking
        url = reverse('booking:booking-delete', kwargs={'pk': nonexistent_booking_id})

        # Perform cancel booking request
        response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)

        # Check response
        self.assertEqual(response.status_code, 404)  # Not found

        # Check ticket availability remains unchanged
        self.assertTicketAvailability(self.ticket, 10)

    def test_create_booking_success(self):
        """ Ensure initial ticket availability """
        initial_availability = self.ticket.availability

        # Valid booking data
        booking_data = {'quantity': 2}

        # URL for booking tickets
        url = reverse('booking:booking-book', kwargs={'event_id': self.event.pk, 'ticket_id': self.ticket.pk})

        # Perform booking request with customer token
        response = self.client.post(url, booking_data, HTTP_AUTHORIZATION='Token ' + self.customer1_token.key)

        # Check response
        self.assertEqual(response.status_code, 201)  # Created

        # Check ticket availability after booking
        updated_ticket = Ticket.objects.get(pk=self.ticket.pk)
        self.assertEqual(updated_ticket.availability, initial_availability - 2)  # Quantity deducted from availability

        # Check booking record created
        self.assertTrue(Booking.objects.filter(customer=self.customer1, event=self.event, ticket=self.ticket, quantity=2).exists())

