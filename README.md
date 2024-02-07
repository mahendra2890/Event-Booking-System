# Event-Booking-System
A backend system for an Event Booking System.
The system has two types of users: Event Organizers and Customers.
Event Organizers can create, read, and update events, while Customers can book tickets for these events.
The API access is restricted based on the user type.

Database Design:
1. Tables:
    - EventOrganizers: Information about the event organizers.
    - Customers: Information about customers.
    - Events: Information about each event, including date, venue, and organizer.
    - Tickets: Types of tickets available for each event, including pricing and availability.
    - Bookings: Information about ticket bookings by customers.

2. Relationships:
    - An Event Organizer can create multiple Events.
    - An Event can have multiple Ticket types (General Admission, VIP, etc.).
    - A Customer can make multiple Bookings.
    - A Booking will relate to a single Event and specific Ticket types.


APIs:
A swagger page has been set up for better accessing/testing API endpoints.
schema can be found in schema.yml function.

To set the project on on your local machine:
1. Install docker.
2. Open terminal, and send the following commands:
    1. docker-compose build                                                 (to install dependencies)
    2. docker-compose up -d                                                 (to bring all services up)
    3. docker-compose run --rm app sh -c "python manage.py makemigrations"  (to create migrations)
    4. docker-compose run --rm app sh -c "python manage.py wait_for_db"     (to make sure the db is started before app)
    5. docker-compose run --rm app sh -c "python manage.py migrate"         (to apply migrate)
    5. docker-compose run --rm app sh -c "python manage.py test"            (to run inbuilt tests)

To stop the server: docker-compose down

The API should be accessible on local host now.
To see available APIs and run (to see how to run : Go to point 3):

1. visit: http://127.0.0.1:8000/api/docs/ :
    This is open up swagger page, where you will see all available APIs, some APIs need authorization to be accessed, and some can be accessed without authorization also.
    1. User Endpoints:
        1. POST ​/api​/user​/create​/: used to create a user: for customer, I have enabled one more field that can be sent as empty - in case we want different inputs for different users
        2. PATCH /api​/user​/me​/ : Can be used to edit user
        3. GET ​/api​/user​/me​/ : Can be used to retrieve user
        4. POST ​/api​/user​/token​/ : can be used to generate token for a user.

    2. Schema Endpoints:
        1. GET ​/api​/schema​/ : can be used to download schema (file schema.yml is downloaded from here)

    3. Event Endpoints:
        1. POST ​/api​/event​/create​/                          : Create an event
        2. POST ​/api​/event​/{event_id}​/tickets​/create​/       : Create a ticket for an event with id=event_id
        3. GET ​/api​/event​/                                  : Retrieve all events
        4. GET ​/api​/event​/{event_id}​/tickets​/               : Retrieve tickets corresponding to an event_id
        5. GET /api​/event​/{id}​/                             : Retrieve information about event with id
        6. GET /api​/event​/myevents​/                         : Retrieve all events corresponding to the authorized organizer
        7. PATCH /api​/event​/{id}​/update​/                    : Update information about event with id
        8. PATCH ​/api​/event​/{event_id}​/tickets​/{id}​/update​/ : Update ticket details.

    4. Booking Endpoints:
        1. POST ​/api​/booking​/{event_id}​/{ticket_id}​/book​/    : Create booking for ticket ticket_id, and event event_id
        2. GET ​/api​/booking​/mybookings​/                      : Retrieve your bookings
        3. GET ​/api​/booking​/myeventbookings​/{event_id}​/      : Retrieve bookings corresponding to events organized by you
        4. DELETE ​/api​/booking​/{id}​/delete​/                  : Delete booking with id
        5. PATCH ​/api​/booking​/{id}​/update​/                   : Update booking (only fields you send will be updated)
        6. PUT ​/api​/booking​/{id}​/update​/                     : update booking (whole object is replaced - haven't been tested, not advised to use)


2. visit: http://127.0.0.1:8000/admin/ :
    1. You will need a superuser to log in here, which can be created by running command: docker-compose run --rm app sh -c "python manage.py createsuperuser". The email id and password you provide here can be used to log into admin page.
    2. The admin page can be used to see how the objects are created and stored.


3. How to use?:
    1. Create user : create a customer user and an organizer user.
    2  Create Token for the user you want to authorize with: On top right corner on swagger page -> click on Authorize, and in APIkey(this is how the token can be setup on postman, if you prefer that): The API key will be : Token {token_string_generated_from_token_api}
    3. Now that you are authorized, you can use get user endpoint and see details of the user you have authorized with.
    4. A customer and An Event Organizer can perform differnt actions - see near the top in description for details
    5. Go to whichever Endpoint you want to test, and see the json sample input/output data for refernce, and execute with your data.
    6. visit: http://127.0.0.1:8000/admin/
        1. Use this to see how objects change with each operation that you perform in swagger page (http://127.0.0.1:8000/api/docs/ )
4. To check celery logs:
    1. run command: docker-compose logs -f celery_worker



Tests are located in each app, under tests/ folder or tests.py file:
1. app/tests.py : celery tests
2. booking/tests/test_bookings_api.py : booking api tests
3. core/tests/: admin, commands, models tests
4. events/tests/test_event_api : event api tests
5. user/tests/test_user_api.py : user api tests

Models:
1. core/models.py

Celery Tasks:
2. core/tasks.py

Code for a particular endpoint:
1. To see code for endpoints:
    1. Go to the app corresponding to the endpoint,
    2. Find view from url
    3. find related models/serializers for the view