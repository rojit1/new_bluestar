from django import forms
from .models import Vendor, ProductPurchase
from root.forms import BaseForm
from product.models import Product

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'contact',]
    
class ProductPurchaseForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.active(),
    )

    field_order = ['vendor', 'price', 'product']

    class Meta:
        model = ProductPurchase
        fields = [
            "product",
            "price",
            "quantity",
            "item_total",
        ]
        widgets = {
            "product": forms.Select(
                attrs={
                    "class": "form-select",
                    "data-control": "select2",
                    "data-placeholder": "Select Product",
                }
            ),
        }
    

    

