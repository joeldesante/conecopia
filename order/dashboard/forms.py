from django import forms

from .models import GlobalSiteSetting
from catalogue.models import Product

class GlobalSiteSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSiteSetting
        fields = [ "value" ]

GlobalSiteSettingsFormSet = forms.modelformset_factory(GlobalSiteSetting, form=GlobalSiteSettingsForm, extra=0)

class ProductAvailableForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ "price", "quantity", "available" ]

ProductAvailableFormSet = forms.modelformset_factory(Product, form=ProductAvailableForm, extra=0)