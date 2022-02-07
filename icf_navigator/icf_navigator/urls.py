"""icf_navigator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from core import views
from users import views as user_views


urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'),
    path('accounts/register/', user_views.register, name='register'),
    path('form/new', views.new_form, name='new_form'),
    path('form/<int:form_id>/', views.form_sections, name='form_sections'),
    path('form/<int:form_id>/<int:section_id>', views.form_main, name='form'),
    path('form/<int:form_id>/<int:section_id>/preview', views.section_preview, name='preview'),
    path('form/<int:form_id>/manage', views.form_manage, name='form_manage'),
    path('form/<int:form_id>/delete', views.form_manage_delete, name='form_manage_delete'),
    path('form/<int:form_id>/print', views.form_print, name='form_print'),
    path('form/<int:form_id>/question/<int:question_id>/<int:section_id>', views.question_main, name='question'),
    path('form/<int:form_id>/edit_text/<int:question_id>', views.edit_text_edit, name='edit_text'),

    path('debug/questions', views.debug_questions, name='debug_questions'),
    path('debug/json_dict/<int:form_id>', views.debug_json, name='debug_json'),

    url(r'^admin/', admin.site.urls),
]
