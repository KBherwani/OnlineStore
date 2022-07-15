from django.contrib import admin

# Register your models here.
from product.models import Categorie, Product, ProductGallery


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "product_code",
        "price",
        "category",
        "manufacturing_date",
        "expiry_date",
        "owner",
        "status",
    ]


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "gallery_image",
    ]


admin.site.register(ProductGallery, ImageGalleryAdmin)
admin.site.register(Categorie, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
