from behave import given, when, then
from django.contrib.auth import get_user_model
import core.models
from behave_django.decorators import fixtures
from django import forms

@fixtures('ynq-fixture.json')
@given(u'A yesno question')
def step_impl(context):
    pass

@fixtures('ft-fixture.json')
@given(u'A free text question')
def step_impl(context):
    pass

@fixtures('ms-fixture.json')
@given(u'A multiselect question')
def step_impl(context):
    pass

@when(u'The first question is selected')
def step_impl(context):
    context.question = core.models.Question.objects.first()

@then(u'The form should have multiple questions')
def many_questions(context):
    count = core.models.Question.objects.count()
    context.test.assertGreater(count, 0)

@then(u'The question should have a form')
def step_impl(context):
    context.test.assertIsInstance(context.question.form(), forms.Form)

@then(u'The form should have radio buttons')
def step_impl(context):
    form = context.question.form()
    context.test.assertIn("<input", form.__html__())
    context.test.assertIn("radio", form.__html__())

@then(u'The form should have a text field')
def step_impl(context):
    form = context.question.form()
    context.test.assertIn("textarea", form.__html__())


@then(u'The form should have multiple checkboxes')
def step_impl(context):
    form = context.question.form()
    count_inputs = form.__html__().count('input')
    context.test.assertGreater(count_inputs, 1)
