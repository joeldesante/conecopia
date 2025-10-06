from django.db import models

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