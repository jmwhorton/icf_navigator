from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model
from django.urls import reverse

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

    def test_should_list_consent_forms(self):
        models.ConsentForm.objects.create(study_name='A')
        models.ConsentForm.objects.create(study_name='B')
        self.assertContains(self.client.get('/'), 'A')
        self.assertContains(self.client.get('/'), 'B')


class ConsentFormTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('testuser@uams.edu', 'testuser')

    def test_requires_login(self):
        response = self.client.post('/form/new', {'name': 'A'})
        self.assertEqual(response.status_code, 302)

    def test_requires_post(self):
        self.client.login(username='testuser@uams.edu', password="testuser")
        response = self.client.get('/form/new')
        self.assertEqual(response.status_code, 405)

    def test_creates_model(self):
        count = models.ConsentForm.objects.count()
        self.client.login(username='testuser@uams.edu', password="testuser")
        self.client.post('/form/new', {'study_name': 'A'})
        self.assertEqual(count + 1, models.ConsentForm.objects.count())
        self.assertEqual('A', models.ConsentForm.objects.last().study_name)

    def test_redirect_on_create(self):
        self.client.login(username='testuser@uams.edu', password="testuser")
        response = self.client.post('/form/new', {'study_name': 'A'})
        cf = models.ConsentForm.objects.last()
        self.assertRedirects(response, reverse('form', args=(cf.pk,)))

    def test_correct_template(self):
        cf = models.ConsentForm.objects.create(study_name="test_study")
        response = self.client.get(reverse('form', args=(cf.pk,)))
        self.assertTemplateUsed(response, 'core/form.html')

class QuestionTestCase(TestCase):
    def test_questions_minimum_spec(self):
        self.assertTrue(models.Question.objects.create(id="1A", order="2.5"))
