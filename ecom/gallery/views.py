from django.shortcuts import render
from django.http import HttpResponseRedirect
from gallery.models import Item, Cart
from gallery.forms import ItemForm

# Create your views here.

def index(request):
    item_list=Item.objects.order_by('name')
    context={'item_list': item_list}
    return render(request, 'gallery/index.html', context)

def upload(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = Item(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], cost=form.cleaned_data['price'], pic=request.FILES['pic'])
            item.save()
            return HttpResponseRedirect('/gallery/')
    form = ItemForm()
    return render(request, 'gallery/upload.html', {'form': form})
    
def detail (request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        item = None
    return render(request, 'gallery/detail.html', {'item': item})

def add_to_cart (request, id):
    if request.user.is_authenticated:
        c = Cart.objects.filter(user=request.user)
        if not c:
            c = Cart()
            c.save()
            request.user.cart.add(c)
        else:
            c = c.get()
        c.addItem(id)
    return HttpResponseRedirect('/gallery/cart/')
    
def view_cart (request):
    if request.user.is_authenticated:
        c = Cart.objects.filter(user=request.user)
        if not c:
            return HttpResponseRedirect('/gallery/')
        cart = c.get()
        items = cart.items.all()
        return render(request, 'gallery/cart.html', {'cart': cart, 'items': items})
    return HttpResponseRedirect('/gallery/')
    
def clear_cart (request):
    if request.user.is_authenticated:
        c = Cart.objects.filter(user=request.user)
        if not c:
            return HttpResponseRedirect('/gallery/')
        cart = c.get()
        cart.clear()
        cart.totalprice=0
        cart.save()
    return HttpResponseRedirect('/gallery/cart/')
    
def remove_item (request, id):
    if request.user.is_authenticated:
        c = Cart.objects.filter(user=request.user)
        if not c:
            return HttpResponseRedirect('/gallery/')
        cart = c.get()
        cart.removeItem(id)
    return HttpResponseRedirect('/gallery/cart/')
    
def checkout (request):
    if request.user.is_authenticated:
        c = Cart.objects.filter(user=request.user)
        if not c:
            return HttpResponseRedirect('/gallery/')
        cart = c.get()
        cart.checkout()
    return HttpResponseRedirect('/gallery/')