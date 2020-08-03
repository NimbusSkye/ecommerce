from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from gallery.models import Item
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
        else:
            return render(request, 'gallery/errors.html', {'form': form})
    form = ItemForm()
    return render(request, 'gallery/upload.html', {'form': form})