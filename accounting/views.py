from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,TemplateView,UpdateView,View
from root.utils import DeleteMixin
from .models import AccountChart
from django.views.generic import TemplateView
from .forms import AccountChartForm
from decimal import Decimal as D
from django.db.models import Q, Sum


class AccountChartMixin:
    model = AccountChart
    form_class = AccountChartForm
    paginate_by = 10
    queryset = AccountChart.objects.prefetch_related('accountsubledger_set')
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


from .models import AccountSubLedger
from .forms import AccountSubLedgerForm
class AccountSubLedgerMixin:
    model = AccountSubLedger
    form_class = AccountSubLedgerForm
    paginate_by = 10
    queryset = AccountSubLedger.objects.all()
    success_url = reverse_lazy('accountsubledger_list')

class AccountSubLedgerList(AccountSubLedgerMixin, ListView):
    template_name = "accounting/accountsubledger_list.html"
    queryset = AccountSubLedger.objects.all()

class AccountSubLedgerDetail(AccountSubLedgerMixin, DetailView):
    template_name = "accountsubledger/accountsubledger_detail.html"

class AccountSubLedgerCreate(AccountSubLedgerMixin, CreateView):
    template_name = "accounting/create.html"

class AccountSubLedgerUpdate(AccountSubLedgerMixin, UpdateView):
    template_name = "update.html"

class AccountSubLedgerDelete(AccountChartMixin, DeleteMixin, View):
    pass


from .models import TblDrJournalEntry, TblCrJournalEntry, TblJournalEntry
from .forms import JournalEntryForm

class JournalEntryCreateView(View):

    def get(self, request):
        form = JournalEntryForm
        return render(request, 'accounting/journal/journal_entry_create.html', {'form':form})
    
    def post(self, request):
        form = JournalEntryForm(request.POST)
        if form.is_valid():

            journal_entry = TblJournalEntry.objects.create(employee_name=request.user.username)

            debit_sub_ledger = request.POST.get('debit_sub_ledger')
            debit_particulars = request.POST.get('debit_particulars')
            debit_amount = D(request.POST.get('debit_amount', 0.0))
            debit_sub_ledger = AccountSubLedger.objects.get(pk=int(debit_sub_ledger))
            debit_sub_ledger_type = debit_sub_ledger.account_chart.account_type


            credit_sub_ledger = request.POST.get('credit_sub_ledger')
            credit_sub_ledger = AccountSubLedger.objects.get(pk=int(credit_sub_ledger))
            credit_sub_ledger_type = credit_sub_ledger.account_chart.account_type
            credit_particulars = request.POST.get('credit_particulars')
            credit_amount = D(request.POST.get('credit_amount', 0.0))



            TblDrJournalEntry.objects.create(sub_ledger=debit_sub_ledger, journal_entry=journal_entry, particulars=debit_particulars, debit_amount=debit_amount)
            TblCrJournalEntry.objects.create(sub_ledger=credit_sub_ledger, journal_entry=journal_entry,particulars=credit_particulars, credit_amount=credit_amount)

            if debit_sub_ledger_type in ['Asset', 'Expense']:
                debit_sub_ledger.total_value =debit_sub_ledger.total_value + debit_amount
                debit_sub_ledger.save()
            elif debit_sub_ledger_type in ['Liability', 'Revenue', 'Equity']:
                debit_sub_ledger.total_value = debit_sub_ledger.total_value - debit_amount
                debit_sub_ledger.save()

            if credit_sub_ledger_type in ['Asset', 'Expense']:
                credit_sub_ledger.total_value = credit_sub_ledger.total_value - credit_amount
                credit_sub_ledger.save()

            elif credit_sub_ledger_type in ['Liability', 'Revenue', 'Equity']:
                credit_sub_ledger.total_value = credit_sub_ledger.total_value + credit_amount
                credit_sub_ledger.save()



        return redirect('journal_list')
        return render(request, 'accounting/journal_entry_create.html', {'form':form})


class JournalEntryView(View):

    def get(self, request, pk=None):
        if pk:
            journal = TblJournalEntry.objects.get(pk=pk)
            credit_details = TblCrJournalEntry.objects.get(journal_entry=journal)
            debit_details = TblDrJournalEntry.objects.get(journal_entry=journal)
            context = {
                'credit': credit_details,
                'debit': debit_details
            }
            return render(request, 'accounting/journal/journal_voucher.html', context)
            
        journal_entries = TblJournalEntry.objects.all()
        return render(request, 'accounting/journal/journal_list.html',  {'journal_entries': journal_entries})


class TrialBalanceView(View):

    def get(self, request):
        trial_balance = []
        total = {'debit_total':0, 'credit_total':0}
        subledgers = AccountSubLedger.objects.all()
        for subled in subledgers:
            data = {}
            data['account']=subled.sub_ledger_name
            account_type = subled.account_chart.account_type
            data['account_head']=account_type

            if account_type in ['Asset', 'Expense']:
                if subled.total_value > 0:
                    data['debit'] = subled.total_value
                    total['debit_total'] += subled.total_value
                    data['credit'] = '-'
                else:
                    data['credit'] = subled.total_value
                    total['credit_total'] += subled.total_value
                    data['debit'] = '-'
            else:
                if subled.total_value > 0:
                    data['credit'] = subled.total_value
                    total['credit_total'] += subled.total_value
                    data['debit'] = '-'
                else:
                    data['debit'] = subled.total_value
                    total['debit_total'] += subled.total_value
                    data['credit'] = '-'
            trial_balance.append(data)
        # trial_balance = sorted(trial_balance, key=lambda x:x['account_head'])
        context = {
            'trial_balance': trial_balance,
            "total": total
        }

        return render(request, 'accounting/trial_balance.html', context)


class ProfitAndLoss(TemplateView):
    template_name = "accounting/profit_and_loss.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses = AccountSubLedger.objects.filter(account_chart__account_type="Expense")
        revenues = AccountSubLedger.objects.filter(account_chart__account_type="Revenue")

        revenue_list= []
        revenue_total = 0
        expense_list= []
        expense_total = 0

        for revenue in revenues:
            revenue_list.append({'title':revenue.sub_ledger_name, 'amount': revenue.total_value})
            revenue_total += revenue.total_value

        for expense in expenses:
            expense_list.append({'title':expense.sub_ledger_name, 'amount': expense.total_value})
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
            sub = AccountSubLedger.objects.filter(account_chart__ledger=ledger, total_value__gt=0)
            if sub:
                asset_dict[ledger.ledger] = sub


        liabilities = AccountChart.objects.filter(Q(account_type="Liability") | Q(account_type="Equity") )
        for ledger in liabilities:
            sub = AccountSubLedger.objects.filter(account_chart__ledger=ledger, total_value__gt=0)
            if sub:
                liability_dict[ledger.ledger] = sub

        asset_total = AccountSubLedger.objects.filter(account_chart__account_type='Asset').aggregate(Sum('total_value')).get('total_value__sum')
        liability_total = AccountSubLedger.objects.filter(Q(account_chart__account_type="Liability") | Q(account_chart__account_type="Equity") )\
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
    