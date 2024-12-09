from django.http import HttpResponse
from django.template import loader
from .models import Product

def index(request):

    products = Product.objects.all().values()
    template = loader.get_template('order.html')
    context = {
        'products': products
    }

    return HttpResponse(template.render(context, request))

def product(request, id):

    product = Product.objects.get(id = id)
    template = loader.get_template('product.html')
    context = {
        'product': product
    }

    return HttpResponse(template.render(context, request))

def cart(request):
    template = loader.get_template('cart.html')
    return HttpResponse(template.render())

def checkout(request):
    template = loader.get_template('checkout.html')
    return HttpResponse(template.render())

def receipt(request):
    template = loader.get_template('receipt.html')
    return HttpResponse(template.render())