from django import forms

from .models import Product, ProductImage

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ "name", "description", "thumbnail", "price", "quantity", "ingredients" ]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [ "image" ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["image"].widget.attrs["disabled"] = True

ProductImagesFormSet = forms.modelformset_factory(
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True,
)

class MultipleProductImagesForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput())