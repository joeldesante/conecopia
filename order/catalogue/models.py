from django.db import models
from django.utils import timezone
from datetime import datetime

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.TextField(blank=True)
    images = models.JSONField(default=list, blank=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    ingredients = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.name}"

class ProductGroup(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(
        'Product',
        related_name='productGroups'
    )

    def __str__(self):
        return f"{self.name}"

class ShoppingCartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class ShoppingCart(models.Model):
    items = models.ManyToManyField(
        'ShoppingCartItem',
        related_name="ShoppingCarts"
    )

    def __str__(self):
        return f"{self.id}"

class Receipt(models.Model):
    firstname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=30)
    email = models.EmailField(),
    address = models.CharField(max_length=255)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.firstname} {self.surname} : {self.id}"
    
class BillOfSale(models.Model):
    stripe_payment_intent = models.CharField(max_length=255, unique=True)
    serialized_shopping_cart = models.JSONField()

class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField(default=dict)