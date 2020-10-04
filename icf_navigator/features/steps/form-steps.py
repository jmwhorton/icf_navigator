from behave import given, when, then
from django.contrib.auth import get_user_model
import core.models
from behave_django.decorators import fixtures

@fixtures('app-fixtures.json')
@given(u'A configured app')
def load_fixtures(context):
    pass

@fixtures('user-fixture.json')
@given(u'An authenticated user')
def skip_login(context):
    context.user = get_user_model().objects.get(email='testuser@uams.edu')
    context.test.client.force_login(context.user)

@when(u'Vists the homepage')
def visit_homepage(context):
    context.response = context.test.client.get("/")

@when(u'Creates form "{form_name}"')
def create_new_form(context, form_name):
    form_details = {'study_name': form_name}
    context.response = context.test.client.post("/form/new",
                                                form_details,
                                                follow=True)

@then(u'They should see a form to create a new form')
def see_new_form(context):
    context.test.assertContains(context.response, 'Create a new')

@then(u'They should not be able to create a new form')
def not_see_new_form(context):
    context.test.assertNotContains(context.response, 'Create a new')

@then(u'Should see "{text}"')
def find_text(context, text):
    context.test.assertContains(context.response, text)

@then(u'Should see multiple questions')
def find_questions(context):
    forms_found = str(context.response.content).count("<form")
    context.test.assertGreater(forms_found, 2)
