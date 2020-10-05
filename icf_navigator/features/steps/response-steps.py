from behave import given, when, then
from django.contrib.auth import get_user_model
import core.models
import users.models
from behave_django.decorators import fixtures

@given(u'The first form')
def step_impl(context):
    context.form = core.models.ConsentForm.objects.first()

@given(u'On a yesnoquestion')
def step_impl(context):
    context.question = core.models.YesNoQuestion.objects.first()

@given(u'On a text question')
def step_impl(context):
    context.question = core.models.FreeTextQuestion.objects.first()

@given(u'On a multiselect question')
def step_impl(context):
    context.question = core.models.MultiSelectQuestion.objects.first()

@when(u'User answers with "{text}"')
def step_impl(context, text):
    url = '/form/{}/question/{}'.format(context.form.pk, context.question.pk)
    context.test.client.post(url, {'text': text})

@when(u'User answers with yes')
def step_impl(context):
    url = '/form/{}/question/{}'.format(context.form.pk, context.question.pk)
    context.test.client.post(url, {'yes': True})

@when(u'User selects "{option}"')
def step_impl(context, option):
    url = '/form/{}/question/{}'.format(context.form.pk, context.question.pk)
    index = context.question.options.index(option)
    context.test.client.post(url, {'options': [index]})


@then(u'"{option}" should be selected')
def step_impl(context, option):
    resp = core.models.Response.objects.get(form=context.form,
                                question=context.question)
    index = context.question.options.index(option)
    context.test.assertIn(str(index), resp.data['options'])

@then(u'The answer should be stored')
def step_impl(context):
    resp = core.models.Response.objects.get(form=context.form,
                                            question=context.question)
    context.test.assertTrue(resp.data['yes'])

@then(u'"{text}" should be stored')
def step_impl(context, text):
    resp = core.models.Response.objects.get(form=context.form,
                                            question=context.question)
    context.test.assertEquals(resp.data['text'], text)
