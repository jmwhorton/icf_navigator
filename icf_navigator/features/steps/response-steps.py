from behave import given, when, then
from django.contrib.auth import get_user_model
import core.models
import users.models
from behave_django.decorators import fixtures

@given(u'The first form')
def step_impl(context):
    context.form = core.models.ConsentForm.objects.first()

@given(u'A yesnoquestion')
def step_impl(context):
    context.question = core.models.YesNoQuestion.objects.first()

@when(u'User answers with yes')
def step_impl(context):
    url = '/form/{}/question/{}'.format(context.form.pk, context.question.pk)
    context.test.client.post(url, {'yes': True})

@then(u'The answer should be stored')
def step_impl(context):
    resp = core.models.Response.objects.get(user=context.user,
                                form=context.form,
                                question=context.question)
    context.test.assertTrue(resp.data['yes'])
