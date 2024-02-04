"""
Database Models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password=None, **extra_fields):
        """create, save and return a new user, email needs to be provided"""
        if not email:
            raise ValueError("user needs to have an email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
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
    is_organiser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
