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
