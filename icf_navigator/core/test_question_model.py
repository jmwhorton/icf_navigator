from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model
from django import forms

class QuestionTestCase(TestCase):
    def test_questions_minimum_spec(self):
        self.assertTrue(models.Question.objects.create())

    def test_questions_return_their_form(self):
        q = models.Question.objects.create()
        self.assertIsInstance(q.form(), forms.Form)

    def test_store_json_in_msq(self):
        a = [1, 2, 3]
        msq = models.MultiSelectQuestion()
        msq.options = a
        msq.save()
        m2 = models.MultiSelectQuestion.objects.first()
        self.assertEqual(a, m2.options)

    def test_msq_form(self):
        a = [1, 2, 3]
        msq = models.MultiSelectQuestion.objects.create(options=a)
        self.assertGreater(len(msq.form().fields['options'].choices), 0)
