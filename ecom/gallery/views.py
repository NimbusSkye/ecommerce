from django.shortcuts import render
from django.http import HttpResponse
from gallery.models import Item

# Create your views here.

def index(request):
    item_list=Item.objects.order_by('-name')
    context={'item_list': item_list}
    return render(request, 'gallery/index.html', context)
    
