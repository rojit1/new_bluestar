from accounting.models import AccountChart, AccountLedger, TblCrJournalEntry, TblJournalEntry, TblDrJournalEntry
from decimal import Decimal

def create_journal_for_bill(instance):
    payment_mode = instance.payment_mode
    grand_total = Decimal(instance.grand_total)
    tax_amount = Decimal(instance.tax_amount)

    if payment_mode == 'Credit':
        pass
    else:
        
        cash_ledger = AccountLedger.objects.get(ledger_name='Cash-In-Hand')
        cash_ledger.total_value = cash_ledger.total_value + grand_total
        cash_ledger.save()

        sale_ledger = AccountLedger.objects.get(ledger_name='Sales')
        sale_ledger.total_value = sale_ledger.total_value+(grand_total-tax_amount)
        sale_ledger.save()

        vat_payable = AccountLedger.objects.get(ledger_name='Vat Payable')
        vat_payable.total_value = vat_payable.total_value + tax_amount
        vat_payable.save()

        journal_entry = TblJournalEntry.objects.create(employee_name='Created Automatically during Sale', journal_total=grand_total)
        TblDrJournalEntry.objects.create(journal_entry=journal_entry, ledger=cash_ledger, debit_amount=grand_total)
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, ledger=sale_ledger, credit_amount=(grand_total-tax_amount))
        TblCrJournalEntry.objects.create(journal_entry=journal_entry, ledger=vat_payable, credit_amount=tax_amount)


        






    

