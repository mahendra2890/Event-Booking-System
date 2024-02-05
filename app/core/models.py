"""
Database Models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError


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
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    role = models.CharField(max_length=20, choices=[('organizer', 'Organizer'), ('customer', 'Customer')], default='customer')
    USERNAME_FIELD = 'email'
    def clean(self):
        super().clean()
        if self.role not in ['organizer', 'customer']:
            raise ValidationError({'role': 'Invalid role'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class EventOrganizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # organizer_specific_field = models.CharField(max_length=255, default='something organizer')
    def save(self, *args, **kwargs):
        # Ensure the associated user has the 'organizer' role
        print(self.user.role)
        if self.user.role != 'organizer':
            raise ValidationError("An EventOrganizer must have the role 'organizer'")

        super().save(*args, **kwargs)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_specific_field = models.CharField(max_length=255, default="SOMETHING CUSTOMER")
    def save(self, *args, **kwargs):
        # Ensure the associated user has the 'customer' role
        if self.user.role != 'customer':
            raise ValidationError("A customer must have the role 'customer'")

        super().save(*args, **kwargs)


class Event(models.Model):
    organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    venue = models.CharField(max_length=255)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.PositiveIntegerField()


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    # Add additional fields as needed.
    def save(self, *args, **kwargs):
        # Ensure quantity is allowed
        if self.quantity > self.ticket.availability or self.quantity <= 0:
            raise ValidationError("Quantity not allowed, allowed quantity > 0 and <= {}".format(self.ticket.availability))
        # Update the availability of the ticket
        self.ticket.availability -= self.quantity
        self.ticket.save()
        super().save(*args, **kwargs)
