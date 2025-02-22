from django.db import models
from django.utils import timezone
from datetime import datetime

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="products/thumbnails", blank=True)
    images = models.JSONField(default=list, blank=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    ingredients = models.JSONField(default=list, blank=True)
    available = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.thumbnail:
            self.thumbnail.delete() # Delte the thumbnail from digital ocean first!
        return super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products/images")
    
    def delete(self, *args, **kwargs):
        if self.image:
            print("Trying to delete")
            self.image.delete() # Deletes the image from digital ocean first before deleting the record.
        super().delete(*args, **kwargs)

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