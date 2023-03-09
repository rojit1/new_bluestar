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

    def __str__(self):
        return self.ledger
    

class AccountSubLedger(AccountBaseModel):
    account_chart = models.ForeignKey(AccountChart, on_delete=models.PROTECT)
    sub_ledger_name = models.CharField(max_length=200, unique=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    affects_cash_flow = models.CharField(max_length=20)

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


class StandardLedgerHead(AccountBaseModel):
    fixed_assets = models.ForeignKey(AccountSubLedger, verbose_name='Fixed Assets', related_name='fixed_assets', on_delete=models.SET_NULL, null=True, blank=True)
    purchase_accounts = models.ForeignKey(AccountSubLedger, verbose_name='Purchase Accounts', related_name='purchase_accounts', on_delete=models.SET_NULL, null=True, blank=True)
    sales_accounts = models.ForeignKey(AccountSubLedger, verbose_name='Sales Account', related_name='sales_accounts', on_delete=models.SET_NULL, null=True, blank=True)
    loans = models.ForeignKey(AccountSubLedger, verbose_name='Loans', related_name='loans', on_delete=models.SET_NULL, null=True, blank=True)
    direct_income = models.ForeignKey(AccountSubLedger, verbose_name='Direct Income', related_name='direct_income', on_delete=models.SET_NULL, null=True, blank=True)
    direct_expenses = models.ForeignKey(AccountSubLedger, verbose_name='Direct Expenses', related_name='direct_expenses', on_delete=models.SET_NULL, null=True, blank=True)
    indirect_income = models.ForeignKey(AccountSubLedger, verbose_name='Indirect Income', related_name='indirect_income', on_delete=models.SET_NULL, null=True, blank=True)
    indirect_expenses = models.ForeignKey(AccountSubLedger, verbose_name='Indirect Expenses', related_name='indirect_expenses', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'Standard Ledger Head'






