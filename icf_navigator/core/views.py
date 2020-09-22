from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Create your views here.
def home_view(request):
    return render(request,
                  'core/home.html',
                  {})
