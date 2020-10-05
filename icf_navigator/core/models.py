from django.db import models
from django import forms
from users.models import ADUser

class ConsentForm(models.Model):
    study_name = models.CharField(max_length=500)

    @property
    def print_dictionary(self):
        dict = {}
        for question in Question.objects.all():
            try:
                response = Response.objects.get(form=self, question=question)
                dict[question.label] = question.for_dict(response.data)
            except Response.DoesNotExist:
                pass
        return dict
    def __str__(self):
        return self.study_name[:20]

class NoQuestionSubtypeException(Exception):
    pass

class Question(models.Model):
    text = models.TextField(blank=True)
    order = models.FloatField(unique=True)
    label = models.CharField(max_length=50, unique=True)
    qtype = models.CharField(max_length=50, default='question')

    def save(self, *args, **kwargs):
        self.qtype = type(self).__name__.lower()
        super().save(*args, **kwargs)

    def __eq__(self, other):
        return self.pk == other.pk

    @property
    def my_type(self):
        try:
            return getattr(self, self.qtype)
        except:
            raise NoQuestionSubtypeException("Had no subclass")

    def form(self, *args, **kwargs):
        return self.my_type.form(*args, **kwargs)

    def for_dict(self, data):
        return self.my_type.for_dict(data)

    def __str__(self):
        return self.label

class Response(models.Model):
    form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    class Meta:
        unique_together = [['form', 'question']]
    def __str__(self):
        return "{}[{}]".format(self.form, self.question)


class YesNoForm(forms.Form):
    yes = forms.TypedChoiceField(label='',
                             required=True,
                             coerce=lambda x: x == 'True',
                             choices=[(True, 'Yes'),(False, 'No')],
                             widget=forms.RadioSelect)

class YesNoQuestion(Question):
    def form(self, *args, **kwargs):
        return YesNoForm(*args, **kwargs)
    def for_dict(self, data):
        return data['yes']

class FreeTextForm(forms.Form):
    text = forms.CharField(label='', required=True, widget=forms.Textarea)

class FreeTextQuestion(Question):
    def form(self, *args, **kwargs):
        return FreeTextForm(*args, **kwargs)
    def for_dict(self, data):
        return data['text']

class MultiSelectForm(forms.Form):
    options = forms.MultipleChoiceField(label='', widget=forms.CheckboxSelectMultiple)
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        c = zip(range(len(choices)), choices)
        self.fields['options'].choices = c

class MultiSelectQuestion(Question):
    options = models.JSONField()
    def form(self, *args, **kwargs):
        return MultiSelectForm(self.options, *args, **kwargs)

    def for_dict(self, data):
        ret = []
        for i in data['options']:
            ret.append(self.options[int(i)])
        return ret

class TextListingForm(forms.Form):
    def __init__(self, num_required, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(num_required):
            f = forms.CharField(label='',
                                required=True,
                                widget=forms.Textarea)
            self.fields['text_{}'.format(i)] = f

class TextListQuestion(Question):
    minimum_required = models.IntegerField()
    allow_more = models.BooleanField(default=False)

    def form(self, *args, **kwargs):
        return TextListingForm(self.minimum_required, *args, **kwargs)

    def for_dict(self, data):
        ret = []
        for key in data.keys():
            ret.append(data[key])
        return ret

class ContactForm(forms.Form):
    title = forms.CharField()
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)

class ContactQuestion(Question):
    def form(self, *args, **kwargs):
        return ContactForm(*args, **kwargs)
    def for_dict(self, data):
        return data

class IntegerForm(forms.Form):
    number = forms.IntegerField(required=True)

class IntegerQuestion(Question):
    def form(self, *args, **kwargs):
        return IntegerForm(*args, **kwargs)
    def for_dict(self, data):
        return data['number']
