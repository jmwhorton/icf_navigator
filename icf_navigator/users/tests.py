from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ADUser, CustomUserManager

# Create your tests here.

class ADUsersTest(TestCase):
    def test_custom_user_works(self):
        self.assertEqual(get_user_model(), ADUser)

    def test_username_must_be_email(self):
        User = get_user_model()
        self.assertTrue(User.objects.create_user('testuser2@uams.edu', 'testuser'))
        self.assertRaises(Exception, User.objects.create_user('testuser', 'testuser'))
