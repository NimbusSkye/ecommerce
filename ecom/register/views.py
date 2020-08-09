from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Cart
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def register(request):
    form=RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/gallery/')
        else:
            form=RegisterForm()
    return render(request, 'register/register.html', {'form': form})
        
        
def create_cart (request):
    if request.user.is_authenticated:
        c = Cart()
        c.save()
        request.user.cart.add(c)
    return HttpResponseRedirect('/gallery/')
    
def add_to_cart (request, item):
    if request.user.is_authenticated:
        request.user.cart.addItem(item)
    return HttpResponseRedirect('/gallery/')