from django import forms

class ItemForm (forms.Form):
    name = forms.CharField(label='Item Name', max_length=100)
    desc = forms.CharField(label='Item Description', max_length=500)
    price = forms.IntegerField(label='Item Price')
    pic = forms.ImageField(label='Item Photo')