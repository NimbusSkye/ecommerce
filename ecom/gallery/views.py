from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Item, Cart, Phone
from .forms import ItemForm, PhoneForm
from django.contrib.auth.models import User
from django.views.generic import ListView

# Create your views here.

class SearchResultsView(ListView):
    model = Item
    template_name = 'gallery/search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Item.objects.filter(name__icontains=query)
            return object_list
        return None
        
def chat(request):
    return render(request, 'gallery/chat.html', None)

def index(request):
    item_list=None
    if request.user.is_authenticated:
        items=Item.objects.all()
        own_items=Item.objects.filter(user=request.user)
        list=items.difference(own_items)
        c=Cart.objects.filter(user=request.user)
        if c:
            cart=c.get()
            list=list.difference(cart.items.all())
        item_list=list.order_by('name')
    return render(request, 'gallery/index.html', {'item_list': item_list})

def blank_upload_form (request, phone):
    form = ItemForm()
    form2 = None
    if not phone:
        form2 = PhoneForm()
    return render(request, 'gallery/upload.html', {'form': form, 'form2': form2})
    
def upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/gallery/')
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
    
def sellerList (request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/gallery/')
    list = Item.objects.filter(user=request.user)
    return render(request, 'gallery/sellerlist.html', {'list': list})
    
def detail (request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/gallery/')
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        item = None
    own_item = False
    if item:
        own_item = request.user == item.user
    return render(request, 'gallery/detail.html', {'item': item, 'own_item': own_item})
    
def delete_listing (request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        item = None
    if item and request.user == item.user:
        item.delete()
    return HttpResponseRedirect('/gallery/sellerlist/')
    
def cartExists (request):
    if request.user.is_authenticated and Cart.objects.filter(user=request.user):
        return True
    return False

def add_to_cart (request, id):
    try:
        item=Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponseRedirect('/gallery/')
    if not request.user.is_authenticated or request.user == item.user:
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/gallery/')
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