from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Item, Cart, Phone
from .forms import ItemForm, PhoneForm
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    item_list=Item.objects.order_by('name')
    context={'item_list': item_list}
    return render(request, 'gallery/index.html', context)

def blank_upload_form (request, phone):
    form = ItemForm()
    form2 = None
    if not phone:
        form2 = PhoneForm()
    return render(request, 'gallery/upload.html', {'form': form, 'form2': form2})
    
def upload(request):
    phone = Phone.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if not phone:
            form2 = PhoneForm(request.POST)
            if form2.is_valid():
                p = Phone(number=form2.cleaned_data['number'])
                p.save()
                request.user.phone.add(p)
            else:
                return blank_upload_form(request, phone)
        if form.is_valid():
            item = Item(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], cost=form.cleaned_data['price'], pic=request.FILES['pic'])
            item.save()
            request.user.items.add(item)
            item.findphone()
            return HttpResponseRedirect('/gallery/')
    return blank_upload_form(request, phone)
    
def detail (request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        item = None
    return render(request, 'gallery/detail.html', {'item': item})
    
def cartExists (request):
    if request.user.is_authenticated and Cart.objects.filter(user=request.user):
        return True
    return False

def add_to_cart (request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/gallery/')
    if not cartExists(request):
        c = Cart()
        c.save()
        request.user.cart.add(c)
    c = Cart.objects.filter(user=request.user)
    cart = c.get()
    cart.addItem(id)
    return HttpResponseRedirect('/gallery/cart/')
    
def view_cart (request):
    if cartExists(request):
        c = Cart.objects.filter(user=request.user)
        cart = c.get()
        items = cart.items.all()
        return render(request, 'gallery/cart.html', {'cart': cart, 'items': items})
    return render(request, 'gallery/cart.html', {'cart': None, 'items': None})
    
def clear_cart (request):
    if cartExists(request):
        c = Cart.objects.filter(user=request.user)
        cart = c.get()
        cart.clear()
        cart.totalprice=0
        cart.save()
    return HttpResponseRedirect('/gallery/cart/')
    
def remove_item (request, id):
    if cartExists(request):
        c = Cart.objects.filter(user=request.user)
        cart = c.get()
        cart.removeItem(id)
    return HttpResponseRedirect('/gallery/cart/')
    
def checkout (request):
    if cartExists(request):
        c = Cart.objects.filter(user=request.user)
        cart = c.get()
        cart.checkout()
    return HttpResponseRedirect('/gallery/')