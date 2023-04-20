from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 

class AccountBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DepreciationPool(models.Model):
    label = models.CharField(max_length=3)
    percentage = models.SmallIntegerField()

    def __str__(self):
        return f'{self.label} - {self.percentage} %'


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
    
    
class AccountSubLedger(AccountBaseModel):
    ledger = models.ForeignKey(AccountLedger, on_delete=models.PROTECT)
    sub_ledger_name = models.CharField(max_length=100)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_ledger_name
    


class TblJournalEntry(AccountBaseModel):
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    journal_total = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return 'Journal Entry'


class TblCrJournalEntry(AccountBaseModel):
    ledger = models.ForeignKey(AccountLedger, on_delete=models.PROTECT)
    sub_ledger = models.ForeignKey(AccountSubLedger, null=True, on_delete=models.SET_NULL)
    journal_entry = models.ForeignKey(TblJournalEntry, on_delete=models.PROTECT)
    particulars = models.TextField(max_length=255)
    credit_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.ledger} -> {self.credit_amount}'


class TblDrJournalEntry(AccountBaseModel):
    ledger = models.ForeignKey(AccountLedger, on_delete=models.PROTECT)
    sub_ledger = models.ForeignKey(AccountSubLedger, null=True, on_delete=models.SET_NULL)
    journal_entry = models.ForeignKey(TblJournalEntry, on_delete=models.PROTECT)
    particulars = models.TextField(max_length=255)
    debit_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.ledger} -> {self.debit_amount}'


class Expense(AccountBaseModel):
    ledger = models.ForeignKey(AccountLedger, related_name='ledger',  on_delete=models.PROTECT)
    sub_ledger = models.ForeignKey(AccountSubLedger, on_delete=models.PROTECT, null=True, blank=True)
    credit_ledger = models.ForeignKey(AccountLedger, related_name='credit_ledger', on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"Expense @ {self.amount}"
    
@receiver(post_save, sender=Expense)
def create_journal_for_expense(sender, instance, **kwargs):
    
    journal = TblJournalEntry.objects.create(employee_name="From expense form", journal_total=instance.amount)
    TblDrJournalEntry.objects.create(ledger=instance.ledger, debit_amount=instance.amount, particulars=f"Automatic: {instance.ledger.ledger_name} a/c Dr", journal_entry=journal)
    TblCrJournalEntry.objects.create(ledger=instance.credit_ledger, credit_amount=instance.amount, particulars=f"Automatic: To {instance.credit_ledger.ledger_name}", journal_entry=journal)

    
    instance.ledger.total_value += instance.amount
    instance.ledger.save()

    if instance.sub_ledger:
        instance.sub_ledger.total_value += instance.amount
        instance.sub_ledger.save()

    instance.credit_ledger.total_value -= instance.amount
    instance.credit_ledger.save()







