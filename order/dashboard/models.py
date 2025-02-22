from django.db import models

class GlobalSiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(default="")

    def __str__(self):
        return self.key