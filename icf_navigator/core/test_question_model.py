from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model
from django import forms

class QuestionTestCase(TestCase):

    def test_store_json_in_msq(self):
        a = [1, 2, 3]
        msq = models.MultiSelectQuestion(text='test',order=1.4)
        msq.options = a
        msq.save()
        m2 = models.MultiSelectQuestion.objects.first()
        self.assertEqual(a, m2.options)

    def test_msq_form(self):
        a = [1, 2, 3]
        msq = models.MultiSelectQuestion.objects.create(text='test',order=1.5, options=a)
        self.assertGreater(len(msq.form().fields['options'].choices), 0)

    def test_yesnoqquestion_has_type(self):
        q = models.YesNoQuestion.objects.create(text='test', order=1.5)
        self.assertEqual(q.type, 'core.yesnoquestion')

    def test_can_delete_question(self):
        q = models.YesNoQuestion.objects.create(text='test', order=1.5)
        self.assertEqual(models.Question.objects.count(), 1)
        self.assertEqual(models.YesNoQuestion.objects.count(), 1)
        q.delete()
        self.assertEqual(models.Question.objects.count(), 0)
        self.assertEqual(models.YesNoQuestion.objects.count(), 0)
