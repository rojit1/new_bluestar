from django import forms
from .models import Vendor, ProductPurchase
from root.forms import BaseForm
from product.models import Product

class VendorForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'contact',]
    
class ProductPurchaseForm(BaseForm, forms.ModelForm):
    DISCOUNT_PERCENTAGE_CHOICES = (
        (0,0),
        (5,5),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),

    ) 

    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.active(),
    )
    sub_total = forms.FloatField()
    discount_percentage = forms.ChoiceField(choices=DISCOUNT_PERCENTAGE_CHOICES)
    discount_amount = forms.FloatField(initial=0.0)


    taxable_amount = forms.FloatField(initial=0.0)
    non_taxable_amount = forms.FloatField(initial=0.0)

    tax_amount = forms.FloatField(initial=0.0)
    grand_total = forms.FloatField()
    amount_in_words = forms.CharField()
    payment_mode = forms.ChoiceField(
        choices=[
            ("", "-----------------"),
            ("Cash", "Cash"),
            ("Credit", "Credit"),
            ("Credit Card", "Credit Card"),
            ("Mobile Payment", "Mobile Payment"),
            ("Complimentary", "Complimentary"),
        ],
        required=True,
    )


    field_order = ['vendor', 'product', 'sub_total', 'discount_percentage', 'discount_amount', 'taxable_amount',
                'non_taxable_amount', 'tax_amount', 'grand_total', 'amount_in_words', 'payment_mode']



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sub_total"].widget.attrs["readonly"] = True
        self.fields["taxable_amount"].widget.attrs["readonly"] = True
        self.fields["non_taxable_amount"].widget.attrs["readonly"] = True
        self.fields["tax_amount"].widget.attrs["readonly"] = True
        self.fields["grand_total"].widget.attrs["readonly"] = True
        self.fields["tax_amount"].label = "VAT Amount"
        self.fields["discount_amount"].widget.attrs["readonly"] = True
        self.fields["amount_in_words"].widget.attrs["readonly"] = True


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
    

    

