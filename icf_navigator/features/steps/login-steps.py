from behave import given, when, then

@when(u'A user logs in with correct credentials')
def send_login(context):
    context.credentials = {'username': 'jrutecht@uams.edu',
                           'password': 'ignore'}
    context.response = context.test.client.post("/login/",
                                                context.credentials,
                                                follow=True)

@when(u'They reload the homepage')
def reload_page(context):
    context.response = context.test.client.get("/")

@then(u'Their username should appear on the page')
def find_username(context):
    context.test.assertContains(context.response, context.credentials['username'])
