from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Item (models.Model):
    name=models.CharField(max_length=30)
    desc=models.CharField(max_length=400)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', null=True)
    phone=PhoneNumberField(null=True)
    cost=models.IntegerField()
    pic=models.ImageField(upload_to='%Y/%m/%d')
    
    def findphone (self):
        self.phone = Phone.objects.filter(user=self.user).get().number
        self.save()
        
    def __str__ (self):
        return f'{self.name}, {self.id}'
        
class Cart (models.Model):
    items = models.ManyToManyField('Item')
    totalprice = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", null=True)
    
    def addItem (self, id):
        self.items.add(id)
        self.totalprice += Item.objects.get(id=id).cost
        self.save()
    
    def removeItem (self, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            item=None
        if item and item in self.items.all():
            self.totalprice -= item.cost
            self.save()
            self.items.remove(item)
        
    def checkout (self):
        for item in self.items.all():
            item.delete()
        self.items.clear()
        self.totalprice=0
        self.save()
        
    def clear (self):
        self.items.clear()
        
    def __str__ (self):
        if self.items.all():
            str=''
            for item in self.items.all():
                str = str + f'{item.name}, ${item.cost}; '
            return str
        else:
            if self.user:
                str=self.user.username
                return str + f"'s empty cart, id {self.id}"  
            return f"Deleted User's empty cart, id {self.id}"
            
class Phone (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone', null=True)
    number = PhoneNumberField()
    
    def __str__ (self):
        return f"{self.user}'s phone, {self.number}"