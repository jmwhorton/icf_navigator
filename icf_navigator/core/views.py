from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from core import models
from django import forms
from django.urls import reverse

# Create your views here.
def home_view(request):
    consent_forms = models.ConsentForm.objects.all()
    return render(request,
                  'core/home.html',
                  {'consent_forms': consent_forms})

class NewConsentForm(forms.Form):
    study_name = forms.CharField()

def form_main(request, form_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    questions = models.Question.objects.all()
    return render(request,
                  'core/form.html',
                  {'consent_form': cf,
                   'questions': questions})

@login_required
def new_form(request):
    if request.method == 'POST':
        form = NewConsentForm(request.POST)
        if form.is_valid():
            study_name = form.cleaned_data['study_name']
            cf = models.ConsentForm.objects.create(study_name=study_name)
            return HttpResponseRedirect(reverse('form', args=(cf.pk,)))
        else:
            return HttpResponse("bad form", status=500)
    else:
        return HttpResponse("require POST", status=405)
