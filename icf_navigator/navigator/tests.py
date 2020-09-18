from django.test import TestCase
from navigator import views

class LoginTestCase(TestCase):
    def test_login_url_resolves(self):
        response = self.client.post("/login/")
        self.assertEqual(response.resolver_match.func, views.login_view)

    def test_login_captures_username(self):
        response = self.client.post("/login/", {'username': 'TestUsername', 'password': 'good'})
        session = self.client.session
        self.assertEqual(session.get('username'), 'TestUsername')

    def test_login_redirects_to_home(self):
        response = self.client.post("/login/")
        self.assertRedirects(response, "/")



class HomeTestCase(TestCase):
    def test_home_resolves(self):
        response = self.client.get("/")
        self.assertEqual(response.resolver_match.func, views.home_view)
