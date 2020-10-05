from django.test import TestCase
from core import views, models
from django.contrib.auth import get_user_model

class PrintGeneratorTest(TestCase):
    fixtures = ['app-fixtures.json']

    @classmethod
    def setUpTestData(self):
        User = get_user_model()
        self.user = User.objects.first()
        self.form = models.ConsentForm.objects.first()

    def test_minimal_callsign(self):
        self.assertTrue(self.form.print_dictionary)

    def test_text_fields_direct_from_label(self):
        q = models.FreeTextQuestion.objects.first()
        response = models.Response.objects.get(form=self.form, question=q)
        user_answer = response.data["text"]
        self.assertEqual(user_answer, q.for_dict(response.data))
        self.assertEqual(user_answer, self.form.print_dictionary[q.label])

    def test_multitext_array(self):
        q = models.TextListQuestion.objects.first()
        response = models.Response.objects.get(form=self.form, question=q)
        answer_one = response.data['text_0']
        self.assertEqual(answer_one, self.form.print_dictionary[q.label][0])

    def test_checkboxes(self):
        q = models.MultiSelectQuestion.objects.first()
        response = models.Response.objects.get(form=self.form, question=q)
        pd = self.form.print_dictionary[q.label]
        for label in pd:
            self.assertIn(label, q.options)
