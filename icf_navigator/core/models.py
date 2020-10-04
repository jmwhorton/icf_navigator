from django.db import models
from django import forms

class ConsentForm(models.Model):
    study_name = models.CharField(max_length=500)

class Question(models.Model):
    def form(self):
        try:
            return self.yesnoquestion.form()
        except:
            return forms.Form()

class YesNoForm(forms.Form):
    yes = forms.BooleanField(required=True,
                             widget=forms.RadioSelect(choices=[(True, 'Yes'),
                                                               (False, 'No')]))

class YesNoQuestion(Question):
    def form(self):
        return YesNoForm()
