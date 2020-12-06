from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import PotentialUser

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

    def test_logged_in_user_should_list_consent_forms(self):
        self.client.login(username='testuser@uams.edu', password="testuser")
        pu, created = PotentialUser.objects.get_or_create(email='testuser@uams.edu')
        a = models.ConsentForm.objects.create(study_name='A')
        a.authorized_users.add(pu)
        a.save()
        b = models.ConsentForm.objects.create(study_name='B')
        b.authorized_users.add(pu)
        b.save()
        self.assertContains(self.client.get('/'), 'A')
        self.assertContains(self.client.get('/'), 'B')


class ConsentFormTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('testuser@uams.edu', 'testuser')

    def test_a_form_has_sections(self):
        section = models.Section.objects.create(name="A", order=1.0, template="none")
        self.assertTrue(section)

    def test_a_section_has_groups(self):
        section = models.Section.objects.create(name="A", order=1.0, template="none")
        group = models.QGroup.objects.create(name="A", order=1.0, section=section)
        self.assertEqual(group.section, section)

    def test_a_group_has_questions(self):
        pass

    def test_a_group_has_logic(self):
        pass

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

    def test_creates_adds_authorized_user(self):
        count = models.ConsentForm.objects.count()
        self.client.login(username='testuser@uams.edu', password="testuser")
        self.client.post('/form/new', {'study_name': 'A'})
        cf = models.ConsentForm.objects.first()
        self.assertTrue(cf.authorized_users.filter(email='testuser@uams.edu').exists())

    def test_redirect_on_create(self):
        self.client.login(username='testuser@uams.edu', password="testuser")
        response = self.client.post('/form/new', {'study_name': 'A'})
        cf = models.ConsentForm.objects.last()
        self.assertRedirects(response, reverse('form_sections', args=(cf.pk,)))

    def test_correct_template(self):
        cf = models.ConsentForm.objects.create(study_name="test_study")
        pu, created = PotentialUser.objects.get_or_create(email='testuser@uams.edu')
        cf.authorized_users.add(pu)
        cf.save()
        response = self.client.get(reverse('form_sections', args=(cf.pk,)))
        self.assertRedirects(response, reverse('login')
                                    + '?next='
                                    + reverse('form_sections', args=(cf.pk,)))
        self.client.login(username='testuser@uams.edu', password="testuser")
        response = self.client.get(reverse('form_sections', args=(cf.pk,)))
        self.assertTemplateUsed(response, 'core/form_sections.html')
