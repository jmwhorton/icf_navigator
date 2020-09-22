from behave import given, when, then
from django.contrib.auth import get_user_model

@when(u'A user logs in with correct credentials')
def login_and_forward(context):
    User = get_user_model()
    User.objects.create_user('testuser@uams.edu', 'testuser')

    credentials = {'username': 'testuser@uams.edu',
                   'password': 'testuser',
                   'next': '/'}
    context.response = context.test.client.post("/accounts/login/",
                                                credentials,
                                                follow=True)

@when(u'Logs out')
def logout(context):
    context.response = context.test.client.get("/accounts/logout/")

@then(u'Their username should appear on the page')
def find_username(context):
    context.test.assertContains(context.response, 'testuser@uams.edu')

@then(u'Their username should not appear on the page')
def find_no_username(context):
    context.test.assertNotContains(context.response, 'testuser@uams.edu')
