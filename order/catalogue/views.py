from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect
from .models import Product, BillOfSale
from django.conf import settings
from nanoid import generate
from .utils import *
import stripe
import os, json

# Do this with an ENV or something
stripe.api_key = os.environ['STRIPE_SECRET_KEY']

### -- Utilities
'''
Returns the rendered cart data that is intended to be passed to various pages which make use of
the data.
'''
def _get_cart_context(request) -> dict:

    if not "shopping_cart" in request.session:
        request.session["shopping_cart"] = {}

    session_cart_data = request.session.get("shopping_cart", {})    # Data in shopping cart is a JSON Dict / { "1": 4, "5": 2 }
    products = Product.objects.filter(id__in=session_cart_data.keys())

    total_order_price = 0
    total_order_quantity = 0
    rendered_shopping_cart = []
    for product in products:
        cart_item = {}
        cart_item["product"] = product
        cart_item["quantity"] = int(session_cart_data[str(product.id)])
        cart_item["total_price"] = product.price * cart_item["quantity"]
        rendered_shopping_cart.append(cart_item)
        
        total_order_quantity = total_order_quantity + cart_item["quantity"]
        total_order_price = total_order_price + cart_item["total_price"]

    return {
        "items": rendered_shopping_cart,
        "total_order_price": total_order_price,
        "total_order_quantity": total_order_quantity
    }

def _get_receipt_context(receipt) -> dict:

    ###### FIXME: The price should be FIXED!!!! If the product changes in price later the receipt data should not change.
    ###### WE MUST SAVE PRICE DATA IN RECEIPT

    receipt_data = json.loads(receipt)
    products = Product.objects.filter(id__in=receipt_data.keys())

    total_order_price = 0
    total_order_quantity = 0
    rendered_shopping_cart = []
    for product in products:
        cart_item = {}
        cart_item["product"] = product
        cart_item["quantity"] = int(receipt_data[str(product.id)])
        cart_item["total_price"] = product.price * cart_item["quantity"]
        rendered_shopping_cart.append(cart_item)
        
        total_order_quantity = total_order_quantity + cart_item["quantity"]
        total_order_price = total_order_price + cart_item["total_price"]

    return {
        "items": rendered_shopping_cart,
        "total_order_price": total_order_price,
        "total_order_quantity": total_order_quantity
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
        "product": product,
        "shopping_cart": shopping_cart,
        "admin_links": [
            {
                "name": "Edit Product Details",
                "href": "/order/product/{id}/edit".format(id=id)
            }
        ]
    }

    return HttpResponse(template.render(context, request))

def product_edit(request, id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to view this resource.")

    product = Product.objects.get(id = id)

    template = loader.get_template('product.edit.html')
    context = {
        "product": product,
        "admin_links": [
            {
                "name": "Return To Product Page",
                "href": "/order/product/{id}".format(id=id)
            }
        ]
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

    client_secret = None
    if shopping_cart["total_order_price"] > 0:
        intent = stripe.PaymentIntent.create(
            amount=shopping_cart["total_order_price"],
            currency="usd",
        )
        client_secret = intent.client_secret

    template = loader.get_template('checkout.html')
    context = {
        "client_secret": client_secret,
        "stripe_public_key": os.environ['STRIPE_PUBLIC_KEY'],
        "shopping_cart": shopping_cart
    }
    return HttpResponse(template.render(context, request))

def receipt(request):
    bill_of_sale_id = request.GET.get("id")
    if bill_of_sale_id == None:
        pass

    bill_of_sale = BillOfSale.objects.get(id = bill_of_sale_id)

    rendered_receipt = _get_receipt_context(bill_of_sale.serialized_shopping_cart)
    shopping_cart = _get_cart_context(request)

    template = loader.get_template('receipt.html')
    context = {
        "shopping_cart": shopping_cart,
        "receipt": rendered_receipt
    }

    return HttpResponse(template.render(context, request))

# Web Functions 
def upload_image(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    id = request.POST["product_id"]
    
    print(request.FILES)
    file = request.FILES.get('file')
    file_name = '{prefix}-{file_name}'.format(prefix=generate(), file_name=file.name)

    save_path = os.path.join(settings.STATICFILES_DIRS[0], 'uploads', file_name)
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    product = Product.objects.get(id=id)
    product.images.append({
        "src": "/static/uploads/{file}".format(file=file_name),
        "alt": "Alt Text"
    })
    product.save()

    return JsonResponse({
        "path": "/static/uploads/{file}".format(file=file_name)
    })

def upload_thumbnail(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    id = request.POST["product_id"]
    
    print(request.FILES)
    file = request.FILES.get('file')
    file_name = '{prefix}-{file_name}'.format(prefix=generate(), file_name=file.name)

    save_path = os.path.join(settings.STATICFILES_DIRS[0], 'uploads', file_name)
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    product = Product.objects.get(id=id)
    product.thumbnail_url = "/static/uploads/{file}".format(file=file_name)
    product.save()

    return JsonResponse({
        "path": "/static/uploads/{file}".format(file=file_name)
    })

def update_product(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    id = request.POST["product_id"]
    name = request.POST["product_name"]
    description = request.POST["product_description"]
    price = request.POST["product_price"]
    quantity = request.POST["product_quantity"]
    ingredients = json.loads(request.POST["product_ingredients"])

    images = json.loads(request.POST["product_images"])
    thumbnail = request.POST["product_thumbnail"]

    # Update Model
    product = Product.objects.get(id=id)
    product.name = name
    product.description = description
    product.price = int(price)
    product.quantity = int(quantity)
    product.ingredients = ingredients

    product.images = images
    product.thumbnail_url = thumbnail
    
    product.save()
    return JsonResponse({})

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

    # Cap the user to the quantity in stock
    product = Product.objects.get(id=product_id)
    if request.session["shopping_cart"][str(product_id)] > product.quantity:
        request.session["shopping_cart"][str(product_id)] = product.quantity

    # Save and quit
    request.session.modified = True
    return JsonResponse({})

def remove_product_from_cart(request):

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
        
    product_id = request.POST["product_id"]

    # Get the shopping cart
    if not "shopping_cart" in request.session:
        request.session["shopping_cart"] = {}

    if str(product_id) in request.session["shopping_cart"]:
        del request.session["shopping_cart"][str(product_id)]

    # Save and quit
    request.session.modified = True
    return JsonResponse({})

def transaction_processed(request):

    # 0. Get the payment intnet in question...
    payment_intent_secret = request.GET.get("payment_intent_client_secret")
    payment_intent_id = request.GET.get("payment_intent")

    if payment_intent_secret == None or payment_intent_id == None:
        return HttpResponseBadRequest() # These arguments are required
    
    payment_intent = stripe.PaymentIntent.retrieve(id=payment_intent_id)
    
    if payment_intent.status != 'succeeded':
        print("Payment Not Succeeded")
        return HttpResponseBadRequest()

    if not "shopping_cart" in request.session:
        return HttpResponseBadRequest("Shopping cart not found")

    # 1. When a payment is sucessfully processed. 
    #       Subtract the qty of the purchased products from the total inventory.

    shopping_cart_context = _get_cart_context(request)
    for item in shopping_cart_context["items"]:
        item["product"].quantity -= item["quantity"]
        item["product"].save()

    # 2. Create a bill of sale record in the database storing the JSON object which
    #       represents the items sold.
    shopping_cart = json.dumps(request.session["shopping_cart"])
    bill_of_sale = BillOfSale(stripe_payment_intent=payment_intent_id, serialized_shopping_cart=shopping_cart)
    bill_of_sale.save()

    # 3. Clear the shopping cart!!! End the session.
    request.session["shopping_cart"] = {}


    # 4. Send an email notification to the customer and the vendor via MailGun or Stripe.
    #       And, If possible send a text message to the vendor to notify them of a sale.

    send_email(
        to_address="joeldesante@gmail.com", 
        from_adress="Tony DeSante <tony@conecopia.com>", 
        subject="Your Conecopia Gelato Receipt.",
        message="Thank you for shopping with us"
    )


    # 5. Redirect the user to the reciept page and display the order details.
    return redirect("/order/receipt?id={bill_of_sale_id}".format(bill_of_sale_id=bill_of_sale.id), permanent=False)


### --- Webhooks ??? (Maybe, Future...)