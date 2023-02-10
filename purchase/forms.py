from django import forms
from .models import Vendor, ProductPurchase
from root.forms import BaseForm
from product.models import Product

class VendorForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'contact',]
    
class ProductPurchaseForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.active(),
    )
    product = forms.ModelMultipleChoiceField(
        queryset=Product.objects.active(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = ProductPurchase
        fields = [
            # "product",
            "price",
            "quantity",
            "item_total",
        ]
    

    widgets = {
        "vendor": forms.Select(
            attrs={
                "class": "form-select",
                "data-control": "select2",
                "data-placeholder": "Select Vendor",
            }
        ),
    }

