from django.test import TestCase
from core import views
from django.contrib.auth import get_user_model

class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user('testuser@uams.edu', 'testuser')

    def test_login_works(self):
        self.client.post("/accounts/login/", {'username': 'testuser@uams.edu', 'password': 'testuser'})
        response = self.client.get("/")
        self.assertEqual(response.context.get('user').email, 'testuser@uams.edu')

    def test_login_redirects_to_home(self):
        response = self.client.post("/accounts/login/",
                                    {'username': 'testuser@uams.edu',
                                     'password': 'testuser',
                                     'next': '/'})
        self.assertRedirects(response, "/")

class HomeTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('testuser@uams.edu', 'testuser')

    def test_home_resolves(self):
        response = self.client.get("/")
        self.assertEqual(response.resolver_match.func, views.home_view)

    def test_logged_in_user_sees_form(self):
        self.client.login(username='testuser@uams.edu', password="testuser")
        self.assertContains(self.client.get('/'), '<form')

    def test_unlogged_user_does_not_see_form(self):
        self.assertNotContains(self.client.get('/'), '<form')
