from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms


class ResponseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user('testuser@uams.edu', 'testuser')
        cls.form = models.ConsentForm.objects.create()
        cls.ynquestion = models.YesNoQuestion.objects.create(text="test",order=1.1)

    def test_minimum_response(self):
        self.assertTrue(models.Response.objects.create(form=self.form,
                                                       question=self.ynquestion))

    def test_stores_json(self):
        r = models.Response.objects.create(form=self.form,
                                           question=self.ynquestion,
                                           data={'yes':True})
        self.assertTrue(r.data['yes'])
