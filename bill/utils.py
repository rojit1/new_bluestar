from accounting.models import AccountChart, AccountLedger, TblCrJournalEntry, TblJournalEntry, TblDrJournalEntry
from accounting.models import AccountSubLedger, AccountLedger, AccountChart
from purchase.models import AccountProductTracking
from decimal import Decimal

def create_journal_for_bill(instance):
    payment_mode = instance.payment_mode
    grand_total = Decimal(instance.grand_total)
    tax_amount = Decimal(instance.tax_amount)

    if payment_mode == 'Credit':
        pass
    elif payment_mode == "Credit Card":
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


def product_sold(instance):
    product = instance.product
    subledgername = f'{product.title} ({product.category.title})'
    quantity_sold = int(instance.product_quantity)
    inventory_expenses_ledger, created = AccountLedger.objects.get_or_create(ledger_name='Inventory Expenses')

    try:
        sub = AccountSubLedger.objects.get(sub_ledger_name=subledgername, ledger__account_chart__account_type='Asset')
        expenses_subledger, _ = AccountSubLedger.objects.get_or_create(sub_ledger_name=subledgername, ledger=inventory_expenses_ledger)

        all_products = AccountProductTracking.objects.filter(product=instance.product, remaining_stock__gt=0).order_by('created_at')
        total_amount = 0
        for product in all_products:
            if product.remaining_stock >= quantity_sold:
                if total_amount <=0:
                    product.remaining_stock -= quantity_sold
                    product.save()
                    sub.total_value -= (product.purchase_rate * quantity_sold)

                    sub.ledger.total_value -= (product.purchase_rate * quantity_sold)
                    sub.ledger.save()

                    expenses_subledger.total_value += (product.purchase_rate * quantity_sold)
                    expenses_subledger.save()

                    inventory_expenses_ledger.total_value += (product.purchase_rate * quantity_sold)
                    inventory_expenses_ledger.save()
                    break
                else:
                    total_amount += (product.purchase_rate * quantity_sold)
                    product.remaining_stock -= quantity_sold
                    product.save()
                    sub.total_value -= total_amount

                    sub.ledger.total_value -= total_amount
                    sub.ledger.save()

                    expenses_subledger.total_value += total_amount
                    expenses_subledger.save()

                    inventory_expenses_ledger.total_value += total_amount
                    inventory_expenses_ledger.save()
            else:
                total_amount += product.purchase_rate * product.remaining_stock
                quantity_sold -= product.remaining_stock
                product.remaining_stock=0
                product.save()

        sub.save()
        
    except AccountSubLedger.DoesNotExist:
        return
    except Exception as e:
        print(e)
    
    sale_ledger = AccountLedger.objects.get(ledger_name='Sales')
    try:
        sale_subledger = AccountSubLedger.objects.get(sub_ledger_name=subledgername, ledger=sale_ledger)
        sale_subledger.total_value += Decimal(instance.amount)
        sale_subledger.save()
    except AccountSubLedger.DoesNotExist:
        AccountSubLedger.objects.create(sub_ledger_name=subledgername, ledger=sale_ledger, total_value=Decimal(instance.amount))





    

