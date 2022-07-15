from django import forms
import datetime

from django.core.exceptions import ValidationError
from django.forms import formset_factory

from product.models import Product, ProductGallery


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "product_code",
            "price",
            "category",
            "manufacturing_date",
            "expiry_date",
            "status",
            "product_image",
        ]
        widgets = {
            "manufacturing_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},

            ),
            "expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        price_updated = cleaned_data.get("price_updated")
        price = cleaned_data.get("price")

        manufacturing_date = cleaned_data.get("manufacturing_date")
        expiry_date = cleaned_data.get("expiry_date")
        if manufacturing_date > expiry_date:
            raise forms.ValidationError({
                                            "expiry_date": "Expiry date cannot be less than Manufacturing Date"})
        return cleaned_data


class ImageGalleryForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = [
            'gallery_image',
        ]


ImageFormset = formset_factory(ImageGalleryForm, extra=1)
