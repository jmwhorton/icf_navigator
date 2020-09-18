from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    return HttpResponse(f'hello {request.session.get("username")}')

def login_view(request):
    request.session['username'] = request.POST.get('username')
    return redirect('home')
