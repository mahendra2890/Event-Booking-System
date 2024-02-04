"""
Test custom django models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successfully(self):
        """Test creating a user with an email is successful """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TeSt3@example.com', 'TeSt3@example.com'],
        ]

        for email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'pass123')
            self.assertEqual(user.email, normalized_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_create_superuser(self):
        """Test creating a superuser"""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
