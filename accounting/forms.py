from django import forms
from root.forms import BaseForm
from .models import AccountChart, TblDrJournalEntry, TblCrJournalEntry, TblJournalEntry

class AccountChartForm(BaseForm, forms.ModelForm):
    class Meta:
        model = AccountChart
        fields = '__all__'


from .models import AccountSubLedger

class AccountSubLedgerForm(BaseForm, forms.ModelForm):
    class Meta:
        model = AccountSubLedger
        fields = '__all__'


class DrJournalEntryForm(BaseForm, forms.ModelForm):
    employee_name = forms.CharField(required=False)
    class Meta:
        model = TblDrJournalEntry
        fields = '__all__'


class CrJournalEntryForm(BaseForm, forms.ModelForm):
    class Meta:
        model = TblCrJournalEntry
        fields = '__all__'
        

class JournalEntryForm(BaseForm, forms.Form):
    debit_sub_ledger = forms.ModelChoiceField(queryset=AccountSubLedger.objects.all(), label='Sub Ledger')
    debit_particulars = forms.CharField(max_length=255, label='Particulars')
    debit_amount = forms.FloatField(initial=0, label='Amount')

    credit_sub_ledger = forms.ModelChoiceField(queryset=AccountSubLedger.objects.all(), label='Sub Ledger')
    credit_particulars = forms.CharField(max_length=255, label='Particulars')
    credit_amount = forms.FloatField(initial=0, label="Amount")

    class Meta:
        widgets = {
                "debit_sub_ledger": forms.Select(
                    attrs={
                        "class": "form-select",
                        "data-control": "select2",
                        "data-placeholder": "Select Product",
                    }
                ),
            }

    


