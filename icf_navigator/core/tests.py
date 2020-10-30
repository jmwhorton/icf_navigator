from django.test import TestCase
from core import views, models
from users.models import PotentialUser
from django.contrib.auth import get_user_model

class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user('testuser@uams.edu', 'testuser')

    def test_login_works(self):
        self.client.post("/accounts/login/",
                            {'username': 'testuser@uams.edu',
                             'password': 'testuser'})
        response = self.client.get("/")
        self.assertEqual(response.context.get('user').email,
                         'testuser@uams.edu')

    def test_login_redirects_to_home(self):
        response = self.client.post("/accounts/login/",
                                    {'username': 'testuser@uams.edu',
                                     'password': 'testuser',
                                     'next': '/'})
        self.assertRedirects(response, "/")
