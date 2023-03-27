from django.db import models

class AccountBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountChart(AccountBaseModel):
    account_type = models.CharField(max_length=100)
    ledger = models.CharField(max_length=100, unique=True)
    financial_statement = models.CharField(max_length=30, null=True, blank=True)
    is_editable = models.BooleanField(default=True)


    def __str__(self):
        return self.ledger
    

class AccountSubLedger(AccountBaseModel):
    account_chart = models.ForeignKey(AccountChart, on_delete=models.PROTECT)
    sub_ledger_name = models.CharField(max_length=200, unique=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    affects_cash_flow = models.CharField(max_length=20)
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_ledger_name
    

class TblJournalEntry(AccountBaseModel):
    employee_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Journal Entry'


class TblCrJournalEntry(AccountBaseModel):
    sub_ledger = models.ForeignKey(AccountSubLedger, on_delete=models.PROTECT)
    journal_entry = models.ForeignKey(TblJournalEntry, on_delete=models.PROTECT)
    particulars = models.TextField(max_length=255)
    credit_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.sub_ledger} -> {self.credit_amount}'


class TblDrJournalEntry(AccountBaseModel):
    sub_ledger = models.ForeignKey(AccountSubLedger, on_delete=models.PROTECT)
    journal_entry = models.ForeignKey(TblJournalEntry, on_delete=models.PROTECT)
    particulars = models.TextField(max_length=255)
    debit_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.sub_ledger} -> {self.debit_amount}'






