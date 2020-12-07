from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from core import models
from users.models import PotentialUser
from django import forms
from django.urls import reverse

# Create your views here.
def home_view(request):
    consent_forms = []
    if request.user.is_authenticated:
        consent_forms = models.ConsentForm.objects.filter(authorized_users__email=request.user.email)
    first_section = models.Section.objects.first().pk
    return render(request,
                  'core/home.html',
                  {'consent_forms': consent_forms,
                   'first_section': first_section})

class NewEmailForm(forms.Form):
    email = forms.EmailField()

@login_required
def form_manage(request, form_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    form = NewEmailForm()
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return redirect('home')
    if request.method == 'POST':
        form = NewEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pu, created = PotentialUser.objects.get_or_create(email=email)
            if not cf.authorized_users.filter(email=email).exists():
                cf.authorized_users.add(pu)
                cf.save()
                form = NewEmailForm()
    return render(request,
                  'core/form_manage.html',
                  {'cf': cf,
                   'form': form})

@login_required
def form_manage_delete(request, form_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    form = NewEmailForm()
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return redirect('home')
    if request.method == 'POST':
        form = NewEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            id = PotentialUser.objects.get(email=email)
            cf.authorized_users.remove(id)
            return redirect('form_manage', cf.id)
    return render(request,
                  'core/form_manage.html',
                  {'cf': cf,
                   'form': form})

class NewConsentForm(forms.Form):
    study_name = forms.CharField()

@login_required
def form_main(request, form_id, section_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return redirect('home')
    sections = models.Section.objects.all()
    section = models.Section.objects.get(pk=section_id)
    pd = cf.print_dictionary
    qgroups = list(filter(lambda x: x.enabled(pd),
                         models.QGroup.objects.filter(section=section)))
    for qgroup in qgroups:
        qgroup.qs = qgroup.questions.all()
        for question in qgroup.qs:
            try:
                r = models.Response.objects.get(form=cf, question=question)
                question.form = question.form(r.data)
            except:
                question.form = question.form()
    return render(request,
                  'core/form.html',
                  {'consent_form': cf,
                   'pd': pd,
                   'section': section,
                   'sections': sections,
                   'qgroups': qgroups})

@login_required
def section_preview(request, form_id, section_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return HttpResponse("")
    section = models.Section.objects.get(pk=section_id)
    if(section.template == 'none'):
        return HttpResponse("")
    pd = cf.print_dictionary
    return render(request,
                  section.template,
                  {'pd': pd})


@login_required
def form_sections(request, form_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return redirect('home')
    sections = models.Section.objects.all()
    return render(request,
                  'core/form_sections.html',
                  {'consent_form': cf,
                   'sections': sections})

def form_print(request, form_id):
    pd = models.ConsentForm.objects.get(pk=form_id).print_dictionary
    return render(request,
                  'core/print_form.html',
                  {'pd': pd})

@login_required
def new_form(request):
    if request.method == 'POST':
        form = NewConsentForm(request.POST)
        if form.is_valid():
            study_name = form.cleaned_data['study_name']
            email = request.user.email
            pu, created = PotentialUser.objects.get_or_create(email=email)
            cf = models.ConsentForm.objects.create(study_name=study_name)
            cf.authorized_users.add(pu)
            cf.save()
            return HttpResponseRedirect(reverse('form_sections', args=(cf.pk,)))
        else:
            return HttpResponse("bad form", status=500)
    else:
        return HttpResponse("require POST", status=405)

@login_required
def question_main(request, form_id, question_id):
    if request.method == 'POST':
        question = models.Question.objects.get(pk=question_id)
        cf = models.ConsentForm.objects.get(pk=form_id)
        form = question.form(request.POST)
        if form.is_valid():
            r, created = models.Response.objects.get_or_create(form=cf,
                                                      question=question)
            r.data = form.cleaned_data
            r.save()
            return HttpResponse("ok", status=200)
        else:
            return HttpResponse("bad form", status=500)
    return HttpResponse("require POST", status=405)
