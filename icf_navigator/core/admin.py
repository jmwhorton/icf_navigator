from django.contrib import admin
from django import forms
from django.apps import apps
from .models import Template
from simple_history.admin import SimpleHistoryAdmin
from django_ace import AceWidget

class TemplateAdminForm(forms.ModelForm):
    class Meta:
        model = Template
        widgets = {
                'content':AceWidget(mode='django', width='800px'),
                }
        fields = '__all__'

class TemplateAdmin(SimpleHistoryAdmin):
    form = TemplateAdminForm

admin.site.register(Template, TemplateAdmin)

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
