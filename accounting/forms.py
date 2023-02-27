from django import forms
from root.forms import BaseForm
from .models import AccountChart

class AccountChartForm(BaseForm, forms.ModelForm):
    class Meta:
        model = AccountChart
        fields = '__all__'