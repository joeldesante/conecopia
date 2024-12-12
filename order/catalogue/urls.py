from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:id>", views.product, name="product"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("receipt", views.receipt, name="receipt"),

    # Web Functions
    path("functions/add_product_to_cart", views.add_product_to_cart, name="add_product_to_cart"),
]