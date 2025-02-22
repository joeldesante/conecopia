from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from catalogue.models import Product
from .models import GlobalSiteSetting

from .forms import GlobalSiteSettingsFormSet, ProductAvailableFormSet

def site_settings(request):

    settings = GlobalSiteSetting.objects.all()
    if request.method == 'POST':
        formset = GlobalSiteSettingsFormSet(request.POST, queryset=settings)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
        return redirect('site_settings')
    else:
        formset = GlobalSiteSettingsFormSet(queryset=settings)
    
    template = loader.get_template("site_settings.html")
    context = {
        "formset": formset,
        "settings": settings
    }

    return HttpResponse(template.render(context, request))


def manage_products(request):

    products = Product.objects.all()

    if request.method == 'POST':
        formset = ProductAvailableFormSet(request.POST, queryset=products)
        if formset.is_valid():
            formset.save()
            return redirect('manage_products')  # Redirect to refresh the page
        else:
            print(formset.errors)
    else:
        formset = ProductAvailableFormSet(queryset=products)

    template = loader.get_template("products.html")
    context = {
        "formset": formset,
        "products": products
    }

    return HttpResponse(template.render(context, request))
