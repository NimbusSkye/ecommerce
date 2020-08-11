from django.shortcuts import render
from .forms import RegisterForm
from django.http import HttpResponseRedirect

# Create your views here.

def register(request):
    form=RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gallery/')
        else:
            form=RegisterForm()
    return render(request, 'register/register.html', {'form': form})