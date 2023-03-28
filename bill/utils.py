from accounting.models import AccountChart, AccountLedger, TblCrJournalEntry, TblJournalEntry, TblDrJournalEntry

def create_journal_for_bill(instance):
    payment_mode = instance.payment_mode

    # grand_total = instance.grand_total

    # if payment_mode == 'Credit':
    #     pass
    # else:
    #     cash_ledger = AccountLedger.objects.get(ledger_name='Cash-In-Hand')
    #     cash_ledger.total_value = cash_ledger.total_value + grand_total

    #     sale_ledger = AccountLedger.objects.get(ledger_name='Sale')

    #     journal_entry = TblJournalEntry.objects.create(employee_name='')
    #     TblDrJournalEntry.objects.create(journal_entry=journal_entry, ledger=cash_ledger, debit_amount=grand_total)
    #     TblCrJournalEntry.objects.create(journal_entry=journal_entry, ledger=sale_ledger)






    

