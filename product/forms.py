from django import forms

from product.models import Product


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
        ]
        widgets = {
            "manufacturing_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},

                ),
            "expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
                ),
        }
