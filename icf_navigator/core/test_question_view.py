from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model

class QuestionViewTests(TestCase):
    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        self.user = User.objects.create_user('testuser@uams.edu', 'testuser')
        self.form = models.ConsentForm.objects.create()
        self.ynquestion = models.YesNoQuestion.objects.create(text='test',order=25.35)
        self.url = '/form/{}/question/{}'.format(self.form.pk, self.ynquestion.pk)

    def test_generates_response(self):
        self.client.force_login(self.user)
        pre_count = models.Response.objects.count()
        resp = self.client.post(self.url, {'yes': True})
        self.assertEqual(resp.status_code, 200)
        post_count = models.Response.objects.count()
        self.assertGreater(post_count, pre_count)
        resp = models.Response.objects.last()
        self.assertEqual(self.form, resp.form)
        self.assertEqual(self.ynquestion, resp.question)
        self.assertTrue(resp.data['yes'])

    def test_requires_login(self):
        resp = self.client.post(self.url, {})
        self.assertNotEqual(resp.status_code, 200)

    def test_msq(self):
        self.client.force_login(self.user)
        options = ['Apple', 'Orange', 'Banana']
        question = models.MultiSelectQuestion.objects.create(text="test",
                                                             order=25.5266,
                                                             label="msq5",
                                                             options=options)
        url = '/form/{}/question/{}'.format(self.form.pk, question.pk)
        self.client.post(url, {'options': [0]})
        resp = models.Response.objects.last()
        self.assertIn('0', resp.data['options'])
