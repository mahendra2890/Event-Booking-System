"""Serializers for user API view"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.models import EventOrganizer, Customer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'role']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # def create(self, validated_data):
    #     """Create and return a new user"""
    #     role = validated_data.pop('role', 'customer')

    #     # Create the user
    #     user = get_user_model().objects.create_user(role=role, **validated_data)

    #     # Additional data for EventOrganizer
    #     if role == 'organizer':
    #         organizer_data = {'user': user}
    #         organizer_serializer = EventOrganizerSerializer(data=organizer_data)
    #         organizer_serializer.is_valid(raise_exception=True)
    #         organizer_serializer.save()

    #     # Additional data for Customer
    #     elif role == 'customer':
    #         customer_data = {'user': user.pk}
    #         customer_serializer = CustomerSerializer(data=customer_data)
    #         customer_serializer.is_valid(raise_exception=True)
    #         customer_serializer.save()

    #     return user


    # def update(self, instance, validated_data):
    #     """Update and return user"""
    #     if 'role' in validated_data:
    #         raise serializers.ValidationError({'role': 'Role can not be updated'})

    #     password = validated_data.pop('password', None)
    #     user = super().update(instance, validated_data)

    #     if password:
    #         user.set_password(password)
    #         user.save()

    #     return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        print(email)
        print(password)
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EventOrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventOrganizer
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class UserApiCreateSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.ChoiceField(required=True,choices=[('organizer', 'Organizer'), ('customer', 'Customer')], write_only=True)
    other_info=serializers.CharField(required=False)
