from behave import given, when, then
from django.contrib.auth import get_user_model

@when(u'An authenticated user')
def skip_login(context):
    User = get_user_model()
    User.objects.create_user('testuser@uams.edu', 'testuser')
    print(User.objects.all())
    context.test.client.login(username='testuser@uams.edu', password="testuser")

@when(u'Vists the homepage')
def visit_homepage(context):
    context.response = context.test.client.get("/")

@then(u'They should see a form to create a new form')
def see_new_form(context):
    context.test.assertContains(context.response, 'Create a new')

@then(u'They should not be able to create a new form')
def not_see_new_form(context):
    context.test.assertNotContains(context.response, 'Create a new')
