from django.db import models
from django import forms
from users.models import ADUser

class ConsentForm(models.Model):
    study_name = models.CharField(max_length=500)

class Question(models.Model):
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
        return forms.Form(*args, **kwargs)

class Response(models.Model):
    user = models.ForeignKey(ADUser, on_delete=models.CASCADE)
    form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)

class YesNoForm(forms.Form):
    yes = forms.BooleanField(required=True,
                             widget=forms.RadioSelect(choices=[(True, 'Yes'),
                                                               (False, 'No')]))

class YesNoQuestion(Question):
    def form(self, *args, **kwargs):
        return YesNoForm(*args, **kwargs)

class FreeTextForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)

class FreeTextQuestion(Question):
    def form(self, *args, **kwargs):
        return FreeTextForm(*args, **kwargs)

class MultiSelectForm(forms.Form):
    options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        c = zip(range(len(choices)), choices)
        self.fields['options'].choices = c

class MultiSelectQuestion(Question):
    options = models.JSONField()
    def form(self, *args, **kwargs):
        return MultiSelectForm(self.options, *args, **kwargs)
