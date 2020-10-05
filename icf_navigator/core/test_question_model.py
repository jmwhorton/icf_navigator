from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model
from django import forms

class QuestionTestCase(TestCase):
    def test_questions_minimum_spec(self):
        self.assertTrue(models.Question.objects.create(text='test',order=1.2))

    def test_base_question_forms_excepts(self):
        q = models.Question.objects.create(text='test', order=1.3)
        with self.assertRaises(models.NoQuestionSubtypeException):
            q.form()

    def test_base_question_dict_excepts(self):
        q = models.Question.objects.create(text='test', order=1.3)
        with self.assertRaises(models.NoQuestionSubtypeException):
            q.for_dict({})

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

    def test_question_has_qtype(self):
        q = models.Question.objects.create(text='test', order=1.5)
        self.assertEqual(q.qtype, 'question')

    def test_yesnoqquestion_has_qtype(self):
        q = models.YesNoQuestion.objects.create(text='test', order=1.5)
        self.assertEqual(q.qtype, 'yesnoquestion')
