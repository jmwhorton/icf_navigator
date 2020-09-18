from behave import given, when, then
from selenium import webdriver

@when(u'I visit the admin page')
def visit_homepage(context):
    pass
    #driver = webdriver.Firefox()
    #print(context.get_url('/admin'))
    #driver.get(context.get_url('/admin'))
    #context.document = driver.page_source

@then(u'The admin login should appear')
def found_admin_login(context):
    pass
    #assert 'Django administration' in context.document
