"""
User Views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from user.serializers import UserSerializer, CustomerSerializer, EventOrganizerSerializer, AuthTokenSerializer,UserApiCreateSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, serializers
from rest_framework.settings import api_settings
from core.models import *


class CreateUserView(APIView):
    """Views for create user API"""
    serializer_class = UserApiCreateSerializer

    def post(self, request, *args, **kwargs):
        """Create a new user - custmor or event organizer"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            role = serializer.validated_data.get('role', 'customer')
            user = User.objects.create_user(email=email, password=password, role=role)
            if role == 'customer':
                customer = Customer.objects.create(user=user, customer_specific_field='thiscamefromview')
                customer_serializer = CustomerSerializer(customer)  # Serialize the customer object
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            elif role == 'organizer':
                event_organizer = EventOrganizer.objects.create(user=user)
                event_organizer_serializer = EventOrganizerSerializer(event_organizer)
                return Response(event_organizer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """Create a token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    #this makes sure we get this in browsable api


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    """Get to get the current user, and Patch to update user"""
    allowed_methods = ['GET', 'PATCH']

    def get_object(self):
        """Get user"""
        print(self.request.user.email)
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Raise a validation error if 'role' is provided during update
        mutable_request = dict(request.data)

        requested_role = mutable_request.get('role')
        requested_email = mutable_request.get('email')

        # Check if 'email' is provided
        if requested_email is not None:
            raise serializers.ValidationError({'email': 'Email cannot be updated'})

        # Check if 'role' is provided
        if requested_role is not None:
            raise serializers.ValidationError({'role': 'Role cannot be updated'})

        user_instance = self.get_object()
        serializer = self.get_serializer(user_instance, data=request.data, partial=True)

        if serializer.is_valid():
            # Update the user instance
            serializer.save()

            # Update associated Customer or EventOrganizer if applicable
            role = user_instance.role
            if role == 'customer':
                customer_instance = user_instance.customer
                customer_serializer = CustomerSerializer(customer_instance, data=request.data.get('customer', {}), partial=True)
                if customer_serializer.is_valid():
                    customer_serializer.save()

            elif role == 'organizer':
                organizer_instance = user_instance.event_organizer
                organizer_serializer = EventOrganizerSerializer(organizer_instance, data=request.data.get('event_organizer', {}), partial=True)
                if organizer_serializer.is_valid():
                    organizer_serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
