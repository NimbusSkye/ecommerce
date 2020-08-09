from django.db import models
from gallery.models import Item
from django.contrib.auth.models import User

# Create your models here.

class Cart (models.Model):
    items = []
    totalprice = 0
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", null=True)
    
    def getTotal (self):
        return self.totalprice
    
    def addItem (self, item):
        self.items.append(item)
        self.totalprice += item.cost
    
    def removeItem (self, num):
        self.totalprice -= self.items[num].cost
        del self.items[num]
        
    def checkout (self):
        for item in self.items:
            Item.objects.filter(id=item.id).delete()
        self.items.clear()
        
    def clear (self):
        self.items.clear()
        
    def __str__ (self):
        str=self.user.username
        if self.items:
            str=''
            for item in self.items:
                str = str + f'{item.name}, ${item.cost};'
            return str
        else:
            return str + f"'s empty cart, id {self.id}"  