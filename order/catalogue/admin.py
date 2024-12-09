from django.contrib import admin
from .models import Product, ProductGroup, ShoppingCart, ShoppingCartItem, Receipt

admin.site.register(Product)
admin.site.register(ProductGroup)
admin.site.register(ShoppingCartItem)
admin.site.register(ShoppingCart)
admin.site.register(Receipt)
