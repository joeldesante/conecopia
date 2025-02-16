from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("product/<int:id>", views.product, name="product"),
    path("product/<int:id>/edit", views.product_edit, name="product_edit"),

    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("receipt", views.receipt, name="receipt"),
    path("settings", views.settings, name="settings"),

    # Web Functions
    path("functions/add_product_to_cart", views.add_product_to_cart, name="add_product_to_cart"),
    path("functions/remove_product_from_cart", views.remove_product_from_cart, name="remove_product_from_cart"),
    path("functions/transaction_processed", views.transaction_processed, name="transaction_processed"),

    path("functions/update_product", views.update_product, name="update_product"),
    path("functions/upload_image", views.upload_image, name="upload_image"),
    path("functions/upload_thumbnail", views.upload_thumbnail, name="upload_thumbnail"),
]