from django.contrib import admin
from .models import Item
from register.models import Cart

# Register your models here.

admin.site.register(Item)
admin.site.register(Cart)