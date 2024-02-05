# Event-Booking-System
A backend system for an Event Booking System.  The system has two types of users: Event Organizers and Customers.  Event Organizers can create, read, and update events, while Customers can book tickets for these events.  The API access is restricted based on the user role.



create tests:
    event can only be created by organisers
    organizer can only update events created by themselves
    ticket can only be created by the organiser of the event
