from django.db import models

class AccountBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountChart(AccountBaseModel):
    account_type = models.CharField(max_length=100)
    group = models.CharField(max_length=100, unique=True)
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return self.group
    

class AccountLedger(AccountBaseModel):
    account_chart = models.ForeignKey(AccountChart, on_delete=models.PROTECT)
    ledger_name = models.CharField(max_length=200, unique=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return self.ledger_name
    

class TblJournalEntry(AccountBaseModel):
    employee_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Journal Entry'


class TblCrJournalEntry(AccountBaseModel):
    ledger = models.ForeignKey(AccountLedger, on_delete=models.PROTECT)
    journal_entry = models.ForeignKey(TblJournalEntry, on_delete=models.PROTECT)
    particulars = models.TextField(max_length=255)
    credit_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.ledger} -> {self.credit_amount}'


class TblDrJournalEntry(AccountBaseModel):
    ledger = models.ForeignKey(AccountLedger, on_delete=models.PROTECT)
    journal_entry = models.ForeignKey(TblJournalEntry, on_delete=models.PROTECT)
    particulars = models.TextField(max_length=255)
    debit_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.ledger} -> {self.debit_amount}'






