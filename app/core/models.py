"""
Database Models
"""
from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password=None, role='customer', **extra_fields):
        """create, save and return a new user, email needs to be provided"""
        if not email:
            raise ValueError("user needs to have an email")
        user = self.model(email=self.normalize_email(email), role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """create, save and return a new user, email needs to be provided"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user for our APIs"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default='User Singh Choudhary')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    role = models.CharField(
        max_length=20,
        choices=[
            ('organizer', 'Organizer'),
            ('customer', 'Customer')
        ],
        default='customer'
    )

    USERNAME_FIELD = 'email'

    def clean(self):
        super().clean()
        if self.role not in ['organizer', 'customer']:
            raise ValidationError({'role': 'Invalid role'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class EventOrganizer(models.Model):
    """Model for Event Organizers. Can add fields other than User"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eventorganizer')
    def save(self, *args, **kwargs):
        """Ensure role-conformance"""
        if self.user.role != 'organizer':
            raise ValidationError("An EventOrganizer must have the role 'organizer'. Cur Role: {}".format(self.user.role))
        super().save(*args, **kwargs)


class Customer(models.Model):
    """Model for Customer"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer_specific_field = models.CharField(max_length=255, default="SOMETHING CUSTOMER")

    def save(self, *args, **kwargs):
        """Ensure role-conformance"""
        if self.user.role != 'customer':
            raise ValidationError("A customer must have the role 'customer'. Cur Role: {}".format(self.user.role))
        super().save(*args, **kwargs)


class Event(models.Model):
    """Model for Event"""
    organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    venue = models.CharField(max_length=255, default='Venue pura')
    description = models.TextField(default="Its a surprise event")
    title = models.CharField(max_length=255, default="Surprise Event")


class Ticket(models.Model):
    """Model for Ticket"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100,default='Surprise Ticket xD')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.11)
    availability = models.PositiveIntegerField(default=1000)


class Booking(models.Model):
    """Model for Booking"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=5)


    def save(self, *args, **kwargs):
        """Ensure availability-conformance"""
        with transaction.atomic():
            if self._state.adding:
                # If it's a new booking, set quantity_difference to the requested quantity
                quantity_difference = self.quantity
            else:
                # Retrieve the previous quantity
                previous_booking = Booking.objects.select_for_update().get(pk=self.pk)
                previous_quantity = previous_booking.quantity
                quantity_difference = self.quantity - previous_quantity

            print(quantity_difference)
            print(self.quantity)
            if quantity_difference > self.ticket.availability or self.quantity <= 0:
                raise ValidationError("Quantity not allowed")

            """Ensure quantity-update"""
            self.ticket.availability -= quantity_difference
            self.ticket.save()
            super().save(*args, **kwargs)



    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Calculate the quantity being deleted
            quantity_deleted = self.quantity

            # Delete the booking
            super().delete(*args, **kwargs)

            # Update the ticket availability
            self.ticket.availability += quantity_deleted
            self.ticket.save()

