# """Tests for user API"""

# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# CREATE_USER_URL = reverse('user:create')
# TOKEN_URL = reverse('user:token')
# ME_URL = reverse('user:me')


# def create_user(**params):
#     """create and return a new user"""
#     return get_user_model().objects.create_user(**params)


# class PublicUserApiTests(TestCase):
#     """Test the public features of user API"""
#     def setUp(self):
#         self.client = APIClient()

#     def test_create_user_success(self):
#         """Test creating a user is successful"""
#         payload = {
#             'email': 'test@example.com',
#             'password': 'testpass',
#             'name': 'Test Name'
#         }
#         res = self.client.post(CREATE_USER_URL, payload)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         user = get_user_model().objects.get(email=payload['email'])
#         self.assertTrue(user.check_password(payload['password']))
#         self.assertNotIn('password', res.data)

#     def test_user_with_email_exists_error(self):
#         """Test error returned if user with email exists"""
#         payload = {
#             'email': 'test@example.com',
#             'password': 'testpass123',
#             'name': 'Test Name',
#         }
#         create_user(**payload)
#         res = self.client.post(CREATE_USER_URL, payload)

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_password_too_short_error(self):
#         """Test error returned if user with email exists"""
#         payload = {
#             'email': 'test@example.com',
#             'password': 'test',
#             'name': 'Test Name',
#         }
#         res = self.client.post(CREATE_USER_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#         user_exists = get_user_model().objects.filter(
#             email=payload['email']
#         ).exists()
#         self.assertFalse(user_exists)

#     def test_create_token_for_user(self):
#         """Test that a token is generated fro valid credentials"""
#         user_details = {
#             'name': 'Test Name',
#             'email': 'test@example.com',
#             'password': 'password',
#         }
#         create_user(**user_details)
#         payload = {
#             'email': user_details['email'],
#             'password': user_details['password'],
#         }
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertIn('token', res.data)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_create_token_bad_credentials(self):
#         """Test error is raised for invalid credentials"""
#         user_details = {
#             'email': 'test@example.com',
#             'password': 'password',
#         }
#         create_user(**user_details)
#         payload = {
#             'email': user_details['email'],
#             'password': 'wroingpass',
#         }
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn('token', res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_create_token_blank_password(self):
#         """Test posting a blank password returns an error"""
#         user_details = {
#             'email': 'test@example.com',
#             'password': 'password',
#         }
#         create_user(**user_details)
#         payload = {
#             'email': user_details['email'],
#             'password': '',
#         }
#         res = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn('token', res.data)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_retrieve_user_unauthorized(self):
#         """Test authentication is required for users"""
#         res = self.client.get(ME_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateApiTests(TestCase):
#     """Test API requests that require authentication"""

#     def setUp(self):
#         self.user = create_user(
#             email='test@example.com',
#             password='password',
#             name='Test Name',
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)

#     def test_retrieve_profile_success(self):
#         """Test retrieving profile for logged in user"""
#         res = self.client.get(ME_URL)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data,{
#             'name': self.user.name,
#             'email': self.user.email,
#             'role': self.user.role,
#         })

#     def test_post_me_not_allowed(self):
#         """Test POST is not allowed for me endpoint"""
#         res = self.client.post(ME_URL, {})
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

#     def test_update_user_profile(self):
#         """Test updating profile for authenticated user"""
#         payload = {'name': 'Updated Name', 'password': 'newPass'}

#         res = self.client.patch(ME_URL, payload)

#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload['name'])
#         self.assertTrue(self.user.check_password(payload['password']))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import User, EventOrganizer, Customer

class UserCreationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_organizer(self):
        url = reverse('user:create')
        data = {
            'email': 'organizer@example.com',
            'password': 'organizer_password',
            'role': 'organizer',
            'name': 'Organizer Name'
        }

        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(EventOrganizer.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer(self):
        url = reverse('user:create')
        data = {
            'email': 'customer@example.com',
            'password': 'customer_password',
            'role': 'customer',
            'name': 'Customer Name'
        }

        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(EventOrganizer.objects.count(), 0)

