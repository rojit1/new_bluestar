from django import forms
from .models import Vendor
from root.forms import BaseForm

class VendorForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'address', 'contact',]
                        