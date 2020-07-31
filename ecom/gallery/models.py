from django.db import models

# Create your models here.

class Item (models.Model):
    name=models.CharField(max_length=30)
    desc=models.CharField(max_length=400)
    cost=models.IntegerField()
    pic=models.CharField(max_length=50)
    
    def __str__ (self):
        return f'{self.name}, {self.desc}'
