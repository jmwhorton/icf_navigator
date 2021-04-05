from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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

    response_text = []

    for qgroup in qgroups:
        qgroup.qs = qgroup.questions.all()
        for question in qgroup.qs:
            try:
                r = models.Response.objects.get(form=cf, question=question)
                question.form = question.form(r.data)

                try:
                    et = models.EditText.objects.get(response=r)
                    question.edit_text = et
                except:
                    question.edit_text = None

                # there is a response do some things
                # Check if canned text exists, add that
                if(models.EditText.objects.filter(response=r).exists()):
                    response_text.append(models.EditText.objects.get(response=r).text)
                elif question.type == 'core.freetextquestion':
                    response_text.append(question.for_dict(r.data))
                else:
                    pass
            except:
                question.form = question.form()
    return render(request,
                  'core/form.html',
                  {'consent_form': cf,
                   'pd': pd,
                   'section': section,
                   'sections': sections,
                   'qgroups': qgroups,
                   'response_text': response_text})

@login_required
def section_preview(request, form_id, section_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return HttpResponse("")
    section = models.Section.objects.get(pk=section_id)
    pd = cf.print_dictionary
    qgroups = list(filter(lambda x: x.enabled(pd),
                         models.QGroup.objects.filter(section=section)))

    response_text = []

    for qgroup in qgroups:
        qgroup.qs = qgroup.questions.all()
        for question in qgroup.qs:
            try:
                r = models.Response.objects.get(form=cf, question=question)
                # there is a response do some things
                # Check if canned text exists, add that
                if(models.EditText.objects.filter(response=r).exists()):
                    response_text.append(models.EditText.objects.get(response=r).text)
                elif question.type == 'core.freetextquestion':
                    response_text.append(question.for_dict(r.data))
                else:
                    pass
            except:
                question.form = question.form()
    if(section.template == 'none'):
        return HttpResponse("")
    return render(request,
                  section.template,
                  {'pd': pd,
                   'response_text': response_text})


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
            if(question.canned):
                et, created = models.EditText.objects.get_or_create(response=r)
                et.text = question.canned.text
                et.save()
            return HttpResponse("ok", status=200)
        else:
            return HttpResponse("bad form", status=500)
    return HttpResponse("require POST", status=405)

@login_required
def edit_text_edit(request, form_id, question_id):
    if request.method == 'POST':
        question = models.Question.objects.get(pk=question_id)
        cf = models.ConsentForm.objects.get(pk=form_id)
        r = models.Response.objects.get(form=cf, question=question)
        form = models.EditTextForm(request.POST)
        if form.is_valid():
            et = models.EditText.objects.get(response=r)
            et.text = form.cleaned_data['text']
            et.save()
            return HttpResponse("ok", status=200)
        else:
            return HttpResponse("bad form", status=500)
    return HttpResponse("require POST", status=405)


@login_required
def debug_questions(request):
    questions = models.Question.objects.all()
    sections = models.Section.objects.all()
    qgroups = models.QGroup.objects.all()
    for qgroup in qgroups:
        qgroup.qs = qgroup.questions.all()
    for question in questions:
        question.warn = False
        question.in_group = False
        for qg in qgroups:
            if question in qg.qs.all():
                if question.in_group == False:
                    question.in_group = qg.name
                else:
                    question.warn = True
                    question.in_group = "MULTIPLE GROUPS {} {}".format(question.in_group, qg.name)
    return render(request, 'core/debug_questions.html',
                    {'questions': questions,
                     'sections': sections,
                     'qgroups': qgroups})

@login_required
def debug_json(request, form_id):
    cf = models.ConsentForm.objects.get(pk=form_id)
    if not cf.authorized_users.filter(email=request.user.email).exists():
        return redirect('home')
    pd = cf.print_dictionary
    return JsonResponse(pd)
