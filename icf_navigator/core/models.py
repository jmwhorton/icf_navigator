from django.db import models
from django import forms
from users.models import ADUser, PotentialUser
from typedmodels.models import TypedModel

class ConsentForm(models.Model):
    study_name = models.CharField(max_length=500)
    authorized_users = models.ManyToManyField(PotentialUser)

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


class Question(TypedModel):
    text = models.TextField(blank=True)
    order = models.FloatField(unique=True)
    label = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['order']

class Response(models.Model):
    form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True)
    class Meta:
        unique_together = [['form', 'question']]
    def __str__(self):
        return "{}[{}]".format(self.form, self.question)

class Section(models.Model):
    name = models.TextField()
    order = models.FloatField(unique=True)
    template = models.TextField()

    def current_count(self):
        return "{} / {}".format('?', '?')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class QGroup(models.Model):
    name = models.TextField(blank=True)
    order = models.FloatField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)
    logic = models.TextField(default='True')

    def __str__(self):
        return self.name

    def enabled(self, pd):
        try:
            ret = eval(self.logic, {'pd': pd})
            return ret
        except:
            return False

    class Meta:
        ordering = ['order']
        unique_together = ['order', 'section']

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

class YesNoExplainForm(forms.Form):
    yes = forms.TypedChoiceField(label='',
                             required=True,
                             coerce=lambda x: x == 'True',
                             choices=[(True, 'Yes'),(False, 'No')],
                             widget=forms.RadioSelect)
    explanation = forms.CharField(label='explain', required=False, widget=forms.Textarea)



class YesNoExplainQuestion(Question):
    YNB_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
        ('B', 'Both')
    ]
    explain_when = models.CharField(null=True, max_length=1, choices=YNB_CHOICES)
    def form(self, *args, **kwargs):
        return YesNoExplainForm(*args, **kwargs)
    def for_dict(self, data):
        return data['explanation']

class FreeTextForm(forms.Form):
    text = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))

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
        self.empty_permitted = True

class MultiSelectQuestion(Question):
    options = models.JSONField(null=True)
    def form(self, *args, **kwargs):
        return MultiSelectForm(self.options, *args, **kwargs)

    def for_dict(self, data):
        ret = []
        if('options' not in data.keys()):
            return ret
        for i in data['options']:
            ret.append(self.options[int(i)])
        return ret

class TextListingForm(forms.Form):
    def __init__(self, num_required, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(num_required):
            f = forms.CharField(label='',
                                required=True,
                                widget=forms.Textarea(attrs={'class': 'form-control'}))
            self.fields['text_{}'.format(i)] = f

class TextListQuestion(Question):
    minimum_required = models.IntegerField(null=True)
    allow_more = models.BooleanField(default=False)

    def form(self, *args, **kwargs):
        return TextListingForm(self.minimum_required, *args, **kwargs)

    def for_dict(self, data):
        ret = []
        for key in data.keys():
            ret.append(data[key])
        return ret

class ContactForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class ContactQuestion(Question):
    def form(self, *args, **kwargs):
        return ContactForm(*args, **kwargs)
    def for_dict(self, data):
        return data

class IntegerForm(forms.Form):
    number = forms.IntegerField(label="", required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class IntegerQuestion(Question):
    def form(self, *args, **kwargs):
        return IntegerForm(*args, **kwargs)
    def for_dict(self, data):
        return data['number']
