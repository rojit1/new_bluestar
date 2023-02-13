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


    sub_total = forms.FloatField()
    grand_total = forms.FloatField()


    field_order = ['vendor', 'product', 'sub_total' ,'grand_total']

    class Meta:
        model = ProductPurchase
        fields = [
            "product",
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
    

    

