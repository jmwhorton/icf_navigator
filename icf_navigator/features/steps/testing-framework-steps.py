from behave import given, when, then
from selenium import webdriver


@given(u'this step exists')
def step_exists(context):
    pass


@when(u'I run "python manage.py behave"')
def run_command(context):
    pass


@then(u'I should see the behave tests run')
def is_running(context):
    pass


@then(u'django_ready should be called')
def django_context(context):
    assert context.django

@when(u'I visit the homepage')
def visit_homepage(context):
    driver = webdriver.Firefox()
    driver.get(context.base_url)
    context.document = driver.page_source


@then(u'Something should be there')
def page_has_content(context):
    assert 'The install worked successfully! Congratulations!' in context.document
