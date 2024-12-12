from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.template import loader
from .models import Product
import stripe

# Do this with an ENV or something
stripe.api_key = "sk_test_51QUwDHCjQ55y9LkRd758BA9JwmiCpNCNK3KqZKle5gObVaIxjGhlWuQtvVqRstRFZVbHVHJTOx72wp7YEfX399wT009GxOrUAk"

### -- Utilities

'''
Returns the rendered cart data that is intended to be passed to various pages which make use of
the data.
'''
def _get_cart_context(request) -> dict:
    session_cart_data = request.session.get("shopping_cart", {})
    products = Product.objects.filter(id__in=session_cart_data.keys())

    total_order_price = 0
    rendered_shopping_cart = []
    for product in products:
        cart_item = {}
        cart_item["product"] = product
        cart_item["quantity"] = int(session_cart_data[str(product.id)])
        cart_item["total_price"] = product.price * cart_item["quantity"]
        rendered_shopping_cart.append(cart_item)

        total_order_price = total_order_price + cart_item["total_price"]

    return {
        "items": rendered_shopping_cart,
        "total_order_price": total_order_price
    }


#### -- Views

def index(request):

    shopping_cart = _get_cart_context(request)

    products = Product.objects.all().values()
    template = loader.get_template('order.html')
    context = {
        "products": products,
        "shopping_cart": shopping_cart
    }

    return HttpResponse(template.render(context, request))

def product(request, id):

    shopping_cart = _get_cart_context(request)

    product = Product.objects.get(id = id)
    template = loader.get_template('product.html')
    context = {
        'product': product,
        "shopping_cart": shopping_cart
    }

    return HttpResponse(template.render(context, request))

def cart(request):
    
    shopping_cart = _get_cart_context(request)

    template = loader.get_template('cart.html')
    context = {
        "shopping_cart": shopping_cart
    }

    return HttpResponse(template.render(context, request))

def checkout(request):

    shopping_cart = _get_cart_context(request)

    intent = stripe.PaymentIntent.create(
        amount=1099,
        currency="usd",
    )

    template = loader.get_template('checkout.html')
    context = {
        "client_secret": intent.client_secret,
        "shopping_cart": shopping_cart
    }
    return HttpResponse(template.render(context, request))

def receipt(request):
    template = loader.get_template('receipt.html')
    return HttpResponse(template.render())

# Web Functions 
def add_product_to_cart(request):

    ##### FIXME: USERS CAN ADD UNLIMITED ITEMS TO CART. LIMIT THIS ON THE BACKEND

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
        
    product_id = request.POST["product_id"]
    quantity = request.POST["quantity"]

    # Get the shopping cart
    if not "shopping_cart" in request.session:
        request.session["shopping_cart"] = {}

    if not str(product_id) in request.session["shopping_cart"]:
        request.session["shopping_cart"][str(product_id)] = int(quantity)
    else:
        request.session["shopping_cart"][str(product_id)] = int(request.session["shopping_cart"][str(product_id)]) + int(quantity)

    # Save and quit
    request.session.modified = True
    
    return JsonResponse()