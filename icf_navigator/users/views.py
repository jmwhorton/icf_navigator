from django.shortcuts import render, redirect
from django.forms import ModelForm
from users.models import ADUser

class UserCreationForm(ModelForm):
    class Meta:
        model = ADUser
        fields = ['email', 'password']


# Create your views here.
def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('home')

    else:
        f = UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})
