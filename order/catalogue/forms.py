from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ "name", "description", "thumbnail", "price", "quantity", "ingredients" ]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [ "image" ]

class MultipleProductImagesForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput())
