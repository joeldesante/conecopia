from django.db import models
from django.utils import timezone
from datetime import datetime
from products.models import Product, ProductImage

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

# TODO: Remove me in favor of GloablSiteSetting
class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField(default=dict)