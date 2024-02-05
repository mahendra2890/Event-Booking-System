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
    serializer_class = UserApiCreateSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user.role == 'customer':
                    customer = Customer.objects.create(user=user, customer_specific_field='thiscamefromview')
                elif user.role == 'organizer':
                    event_organizer = EventOrganizer.objects.create(user=user)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class CreateUserView(generics.CreateAPIView):
#     """Create a new user in the system"""
#     serializer_class = UserSerializer


#     def create(self, request, *args, **kwargs):
#         # Extract role from the request data
#         role = request.data.pop('role', 'customer')

#         # Validate the role
#         if role not in ['organizer', 'customer']:
#             raise serializers.ValidationError({'role': 'Invalid role'})

#         # Create a user with the specified role
#         user_serializer = self.get_serializer(data=request.data)
#         user_serializer.is_valid(raise_exception=True)
#         user = user_serializer.save(role=role)

#         # Additional data for EventOrganizer
#         if user.role == 'organizer':
#             organizer_data = {'user': user.pk}
#             organizer_serializer = EventOrganizerSerializer(data=organizer_data)
#             organizer_serializer.is_valid(raise_exception=True)
#             organizer_serializer.save()

#         # Additional data for Customer
#         elif user.role == 'customer':
#             customer_data = {'user': user.pk}
#             customer_serializer = CustomerSerializer(data=customer_data)
#             customer_serializer.is_valid(raise_exception=True)
#             customer_serializer.save()

#         headers = self.get_success_headers(user_serializer.data)
#         return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class CreateTokenView(ObtainAuthToken):
    """Create a new token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    #this makes sure we get this in browsable api


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET', 'PATCH']
    # queryset = get_user_model().objects.all()  # Set the queryset to the user model

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Raise a validation error if 'role' is provided during update
        current_role = self.request.user.role
        requested_role = request.data.get('role')

        # Check if 'role' is provided and if it matches the current role
        if requested_role is not None and requested_role != current_role:
            raise serializers.ValidationError({'role': 'Role cannot be updated to a different value.'})

        # If 'role' matches, remove it from the request data before passing to the serializer
        if 'role' in request.data:
            del request.data['role']

        return super().update(request, *args, **kwargs)