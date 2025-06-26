from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['title', 'description', 'thumbnail', 'category', 'price', 'stock', 'made_in']