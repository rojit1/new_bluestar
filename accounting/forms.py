from django import forms
from root.forms import BaseForm
from .models import AccountChart, TblDrJournalEntry, TblCrJournalEntry, TblJournalEntry
from django.contrib.admin.widgets import FilteredSelectMultiple

class AccountChartForm(BaseForm, forms.ModelForm):
    class Meta:
        model = AccountChart
        exclude = 'is_editable',


from .models import AccountSubLedger

class AccountSubLedgerForm(BaseForm, forms.ModelForm):
    class Meta:
        model = AccountSubLedger
        exclude = 'is_editable',


class DrJournalEntryForm(BaseForm, forms.ModelForm):
    employee_name = forms.CharField(required=False)
    class Meta:
        model = TblDrJournalEntry
        fields = '__all__'


class CrJournalEntryForm(BaseForm, forms.ModelForm):
    class Meta:
        model = TblCrJournalEntry
        fields = '__all__'
        

class JournalEntryForm(forms.Form):
    debit_sub_ledger = forms.ModelChoiceField(queryset=AccountSubLedger.objects.all())
    debit_particulars = forms.CharField(max_length=255)
    debit_amount = forms.FloatField(initial=0,)

    credit_sub_ledger = forms.ModelChoiceField(queryset=AccountSubLedger.objects.all())
    credit_particulars = forms.CharField(max_length=255)
    credit_amount = forms.FloatField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["debit_sub_ledger"].widget.attrs["class"] = 'form-select'
        self.fields["debit_sub_ledger"].widget.attrs["data-control"] = 'select2'

        self.fields["credit_sub_ledger"].widget.attrs["class"] = 'form-select'
        self.fields["credit_sub_ledger"].widget.attrs["data-control"] = 'select2'



    


