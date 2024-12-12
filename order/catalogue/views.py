from django.http import HttpResponse
from django.template import loader
from .models import Product
import stripe

# Do this with an ENV or something
stripe.api_key = "sk_test_51QUwDHCjQ55y9LkRd758BA9JwmiCpNCNK3KqZKle5gObVaIxjGhlWuQtvVqRstRFZVbHVHJTOx72wp7YEfX399wT009GxOrUAk"

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

    intent = stripe.PaymentIntent.create(
        amount=1099,
        currency="usd",
    )

    template = loader.get_template('checkout.html')
    context = {
        'client_secret': intent.client_secret
    }
    return HttpResponse(template.render(context, request))

def receipt(request):
    template = loader.get_template('receipt.html')
    return HttpResponse(template.render())