from django.db import models
from django import forms

class ConsentForm(models.Model):
    study_name = models.CharField(max_length=500)

class Question(models.Model):
    def form(self):
        try:
            return self.yesnoquestion.form()
        except:
            pass
        try:
            return self.freetextquestion.form()
        except:
            pass
        try:
            return self.multiselectquestion.form()
        except:
            pass
        return forms.Form()

class YesNoForm(forms.Form):
    yes = forms.BooleanField(required=True,
                             widget=forms.RadioSelect(choices=[(True, 'Yes'),
                                                               (False, 'No')]))

class YesNoQuestion(Question):
    def form(self):
        return YesNoForm()

class FreeTextForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)

class FreeTextQuestion(Question):
    def form(self):
        return FreeTextForm()

class MultiSelectForm(forms.Form):
    options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        c = zip(range(len(choices)), choices)
        self.fields['options'].choices = c

class MultiSelectQuestion(Question):
    options = models.JSONField()
    def form(self):
        return MultiSelectForm(self.options)
