from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,TemplateView,UpdateView,View
from root.utils import DeleteMixin
from .models import AccountChart
from django.views.generic import TemplateView
from .forms import AccountChartForm
from decimal import Decimal as D
from django.db.models import Q, Sum
from django.contrib import messages


class AccountChartMixin:
    model = AccountChart
    form_class = AccountChartForm
    paginate_by = 10
    queryset = AccountChart.objects.prefetch_related('accountledger_set')
    success_url = reverse_lazy('accountchart_list')


class AccountChartList(AccountChartMixin, ListView):
    queryset = AccountChart.objects.all()
    template_name = "accounting/accounting_chart.html"


    def get(self, request, *args, **kwargs):
        query_set = self.queryset
        assets = query_set.filter(account_type='Asset')
        liabilities = query_set.filter(account_type='Liability')
        equities = query_set.filter(account_type='Equity')
        revenues = query_set.filter(account_type='Revenue')
        expenses = query_set.filter(account_type='Expense')
        others = query_set.filter(account_type='Other')


        context = {
            'assets': assets,
            'liabilities':liabilities,
            'equities':equities,
            'revenues':revenues,
            'expenses': expenses,
            'others': others
        }
        return render(request, 'accounting/accounting_chart.html', context)



class AccountChartDetail(AccountChartMixin, DetailView):
    template_name = "accounting/accountchart_detail.html"

class AccountChartCreate(AccountChartMixin, CreateView):
    template_name = "accounting/create.html"

class AccountChartUpdate(AccountChartMixin, UpdateView):
    template_name = "update.html"

class AccountChartDelete(AccountChartMixin, DeleteMixin, View):
    pass


from .models import AccountLedger
from .forms import AccountLedgerForm
class AccountLedgerMixin:
    model = AccountLedger
    form_class = AccountLedgerForm
    paginate_by = 10
    queryset = AccountLedger.objects.all()
    success_url = reverse_lazy('accountledger_list')

class AccountLedgerList(AccountLedgerMixin, ListView):
    template_name = "accounting/accountledger_list.html"
    queryset = AccountLedger.objects.all()

class AccountLedgerDetail(AccountLedgerMixin, DetailView):
    template_name = "accounting/accountledger_detail.html"

class AccountLedgerCreate(AccountLedgerMixin, CreateView):
    template_name = "accounting/create.html"

class AccountLedgerUpdate(AccountLedgerMixin, UpdateView):
    template_name = "update.html"

class AccountLedgerDelete(AccountChartMixin, DeleteMixin, View):
    pass


from .forms import AccountSubLedgerForm
class AccountSubLedgerCreate(CreateView):
    template_name = "accounting/subledger/create.html"
    form_class = AccountSubLedgerForm
    success_url = reverse_lazy('accountchart_list')



from .models import TblDrJournalEntry, TblCrJournalEntry, TblJournalEntry, AccountSubLedger
from .forms import JournalEntryForm

class JournalEntryCreateView(View):

    def get(self, request):
        ledgers = AccountLedger.objects.all()
        sub_ledgers = AccountSubLedger.objects.all()
        return render(request, 'accounting/journal/journal_entry_create.html', {'ledgers':ledgers, 'sub_ledgers':sub_ledgers})
    
    def get_subledger(self, subledger, ledger):
        subled = None
        if not subledger.startswith('-'):
            try:
                subledger_id = int(subledger)
                subled = AccountSubLedger.objects.get(pk=subledger_id)
            except ValueError:
                subled = AccountSubLedger.objects.create(sub_ledger_name=subledger, is_editable=True, ledger=ledger)
        return subled
    
    def post(self, request):
        data = request.POST
        debit_ledgers = data.getlist('debit_ledger', [])
        debit_particulars = data.getlist('debit_particular', [])
        debit_amounts = data.getlist('debit_amount', [])
        debit_subledgers = data.getlist('debit_subledger', [])

        credit_ledgers = data.getlist('credit_ledger', [])
        credit_particulars = data.getlist('credit_particular', [])
        credit_amounts = data.getlist('credit_amount', [])
        credit_subledgers = data.getlist('credit_subledger', [])

        ledgers = AccountLedger.objects.all()
        sub_ledgers = AccountSubLedger.objects.all()

        try:
            parsed_debitamt = (lambda x: [D(i) for i in x])(debit_amounts)
            parsed_creditamt = (lambda x: [D(i) for i in x])(credit_amounts)
        except Exception:
            messages.error(request, "Please Enter valid amount")
            return render(request, 'accounting/journal/journal_entry_create.html', {'ledgers':ledgers, 'sub_ledgers':sub_ledgers})
        
        debit_sum, credit_sum = sum(parsed_debitamt), sum(parsed_creditamt)
        if debit_sum != credit_sum:
            messages.error(request, "Debit Total and Credit Total must be equal")
            return render(request, 'accounting/journal/journal_entry_create.html', {'ledgers':ledgers, 'sub_ledgers':sub_ledgers})

        for dr in debit_ledgers:
            if dr.startswith('-'):
                messages.error(request, "Ledger must be selected")
                return render(request, 'accounting/journal/journal_entry_create.html', {'ledgers':ledgers, 'sub_ledgers':sub_ledgers}) 

        journal_entry = TblJournalEntry.objects.create(employee_name=request.user.username, journal_total=debit_sum)
        for i in range(len(debit_ledgers)):
            debit_ledger_id = int(debit_ledgers[i])
            debit_ledger = AccountLedger.objects.get(pk=debit_ledger_id)
            debit_particular = debit_particulars[i]
            debit_amount = D(debit_amounts[i])
            subledger = self.get_subledger( debit_subledgers[i], debit_ledger)
            debit_ledger_type = debit_ledger.account_chart.account_type
            TblDrJournalEntry.objects.create(ledger=debit_ledger, journal_entry=journal_entry, particulars=debit_particular, debit_amount=debit_amount, sub_ledger=subledger)
            if debit_ledger_type in ['Asset', 'Expense']:
                debit_ledger.total_value =debit_ledger.total_value + debit_amount
                debit_ledger.save()
                if subledger:
                    subledger.total_value = subledger.total_value + debit_amount
                    subledger.save()

            elif debit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                debit_ledger.total_value = debit_ledger.total_value - debit_amount
                debit_ledger.save()
                if subledger:
                    subledger.total_value = subledger.total_value - debit_amount
                    subledger.save()

        for i in range(len(credit_ledgers)):
            credit_ledger_id = int(credit_ledgers[i])
            credit_ledger = AccountLedger.objects.get(pk=credit_ledger_id)
            credit_particular = credit_particulars[i]
            credit_amount = D(credit_amounts[i])
            subledger = self.get_subledger( credit_subledgers[i], credit_ledger)
            credit_ledger_type = credit_ledger.account_chart.account_type
            TblCrJournalEntry.objects.create(ledger=credit_ledger, journal_entry=journal_entry, particulars=credit_particular, credit_amount=credit_amount, sub_ledger=subledger)
            if credit_ledger_type in ['Asset', 'Expense']:
                credit_ledger.total_value = credit_ledger.total_value - credit_amount
                credit_ledger.save()
                if subledger:
                    subledger.total_value = subledger.total_value - credit_amount
                    subledger.save()
            elif credit_ledger_type in ['Liability', 'Revenue', 'Equity']:
                credit_ledger.total_value = credit_ledger.total_value + credit_amount
                credit_ledger.save()
                if subledger:
                    subledger.total_value = subledger.total_value + credit_amount
                    subledger.save()

        return redirect('journal_list')


class JournalEntryView(View):

    def get(self, request, pk=None):
        if pk:
            journal = TblJournalEntry.objects.get(pk=pk)
            credit_details = TblCrJournalEntry.objects.filter(journal_entry=journal)
            debit_details = TblDrJournalEntry.objects.filter(journal_entry=journal)
            debit_total, credit_total = 0, 0
            for dr in debit_details:
                debit_total += dr.debit_amount

            for cr in credit_details:
                credit_total += cr.credit_amount

            context = {
                'credit': credit_details,
                'debit': debit_details,
                "dr_total":debit_total,
                "cr_total": credit_total
            }
            return render(request, 'accounting/journal/journal_voucher.html', context)
            

        journal_entries = TblJournalEntry.objects.prefetch_related('tbldrjournalentry_set').all()
        return render(request, 'accounting/journal/journal_list.html',  {'journal_entries': journal_entries})


class TrialBalanceView(View):

    def get(self, request):
        trial_balance = []
        total = {'debit_total':0, 'credit_total':0}
        ledgers = AccountLedger.objects.filter(total_value__gt=0)
        for led in ledgers:
            data = {}
            data['ledger']=led.ledger_name
            account_type = led.account_chart.account_type
            data['account_head']=account_type

            if account_type in ['Asset', 'Expense']:
                if led.total_value > 0:
                    data['debit'] = led.total_value
                    total['debit_total'] += led.total_value
                    data['credit'] = '-'
                else:
                    data['credit'] = led.total_value
                    total['credit_total'] += led.total_value
                    data['debit'] = '-'
            else:
                if led.total_value > 0:
                    data['credit'] = led.total_value
                    total['credit_total'] += led.total_value
                    data['debit'] = '-'
                else:
                    data['debit'] = led.total_value
                    total['debit_total'] += led.total_value
                    data['credit'] = '-'
            trial_balance.append(data)

        vat_receivable, vat_payable = 0, 0
        for data in trial_balance:
            if data['ledger'] == 'VAT Receivable':
                vat_receivable = data['debit']
                total['debit_total'] -= data['debit']
                trial_balance.remove(data)
            if data['ledger'] == 'VAT Payable':
                vat_payable = data['credit']
                total['credit_total'] -= data['credit']
                trial_balance.remove(data)
        vat_amount = vat_receivable - vat_payable
        if vat_amount > 0:
            trial_balance.append({'ledger':'VAT', 'account_head':'Asset', 'debit':vat_amount, 'credit':'-'})
            total['debit_total'] += vat_amount
        elif vat_amount < 0:
            trial_balance.append({'ledger':'VAT', 'account_head':'Liability', 'debit':'-', 'credit':abs(vat_amount)})
            total['credit_total'] += abs(vat_amount)

        trial_balance = sorted(trial_balance, key=lambda x:x['account_head'])
        context = {
            'trial_balance': trial_balance,
            "total": total
        }

        return render(request, 'accounting/trial_balance.html', context)


class ProfitAndLoss(TemplateView):
    template_name = "accounting/profit_and_loss.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses = AccountLedger.objects.filter(account_chart__account_type="Expense", total_value__gt=0)
        revenues = AccountLedger.objects.filter(account_chart__account_type="Revenue", total_value__gt=0)

        revenue_list= []
        revenue_total = 0
        expense_list= []
        expense_total = 0

        for revenue in revenues:
            revenue_list.append({'title':revenue.ledger_name, 'amount': revenue.total_value})
            revenue_total += revenue.total_value

        for expense in expenses:
            expense_list.append({'title':expense.ledger_name, 'amount': expense.total_value})
            expense_total += expense.total_value

        context['expenses'] = expense_list
        context['expense_total'] = expense_total
        context['revenues'] = revenue_list
        context['revenue_total'] = revenue_total

        return context
    

class BalanceSheet(TemplateView):
    template_name = "accounting/balance_sheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        asset_dict = {}
        liability_dict = {}

        assets = AccountChart.objects.filter(account_type='Asset')
        for ledger in assets:
            sub = AccountLedger.objects.filter(account_chart__group=ledger, total_value__gt=0)
            if sub:
                asset_dict[ledger.group] = sub


        liabilities = AccountChart.objects.filter(Q(account_type="Liability") | Q(account_type="Equity") )
        for ledger in liabilities:
            sub = AccountLedger.objects.filter(account_chart__group=ledger, total_value__gt=0)
            if sub:
                liability_dict[ledger.group] = sub

        asset_total = AccountLedger.objects.filter(account_chart__account_type='Asset').aggregate(Sum('total_value')).get('total_value__sum')
        liability_total = AccountLedger.objects.filter(Q(account_chart__account_type="Liability") | Q(account_chart__account_type="Equity") )\
                                    .aggregate(Sum('total_value')).get('total_value__sum')
        

        if asset_total and liability_total:
            if asset_total > liability_total:
                context['lib_retained_earnings'] =  asset_total-liability_total
                context['liability_total'] = liability_total + asset_total-liability_total
                context['asset_total'] = asset_total

            else:
                context['asset_retained_earnings'] =  liability_total-asset_total
                context['asset_total'] = asset_total + liability_total-asset_total
                context['liability_total'] = liability_total
            

        context['assets'] = asset_dict
        context['liabilities'] =  liability_dict

        return context
    