from django.db import models

# Create your models here.
from OnlineStore import settings


class Categorie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    product_code = models.CharField(max_length=100, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    price_updated = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    status = models.CharField(max_length=200, blank=False, null=False)
    product_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gallery_image = models.ImageField(blank=True, null=True)

