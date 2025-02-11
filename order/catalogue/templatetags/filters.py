from django import template
from ..models import Product

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.simple_tag(takes_context=True)
def product_quantity_excluding_cart(context, product_id):
    products_in_cart = context.request.session["shopping_cart"]

    product = Product.objects.get(id=int(product_id))
    if str(product_id) in products_in_cart:
        return product.quantity - int(products_in_cart[str(product_id)])
    
    return product.quantity