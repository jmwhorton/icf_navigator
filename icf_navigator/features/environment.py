"""
behave environment module for testing behave-django
"""


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    pass


def django_ready(context):
    context.django = True
