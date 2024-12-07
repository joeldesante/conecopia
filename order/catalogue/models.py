from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}"