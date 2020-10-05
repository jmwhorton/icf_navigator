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

class Question(models.Model):
    text = models.TextField(blank=True)
    order = models.FloatField(unique=True)
    label = models.CharField(max_length=50, unique=True)

    def __eq__(self, other):
        return self.pk == other.pk

    def form(self, *args, **kwargs):
        try:
            return self.yesnoquestion.form(*args, **kwargs)
        except:
            pass
        try:
            return self.freetextquestion.form(*args, **kwargs)
        except:
            pass
        try:
            return self.multiselectquestion.form(*args, **kwargs)
        except:
            pass
        try:
            return self.textlistquestion.form(*args, **kwargs)
        except:
            pass
        print("Couldn't find a form, probably an error.")
        return forms.Form(*args, **kwargs)

    def for_dict(self, data):
        try:
            return self.yesnoquestion.for_dict(data)
        except:
            pass
        try:
            return self.freetextquestion.for_dict(data)
        except:
            pass
        try:
            return self.multiselectquestion.for_dict(data)
        except:
            pass
        try:
            return self.textlistquestion.for_dict(data)
        except:
            pass
        print("Couldn't find a subtype, probably an error.")
        return data

class Response(models.Model):
    form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    class Meta:
        unique_together = [['form', 'question']]


class YesNoForm(forms.Form):
    yes = forms.BooleanField(label='',
                             required=True,
                             widget=forms.RadioSelect(choices=[(True, 'Yes'),
                                                               (False, 'No')]))

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
