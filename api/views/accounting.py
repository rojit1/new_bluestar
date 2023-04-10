from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from accounting.models import AccountChart, AccountLedger, TblCrJournalEntry, TblDrJournalEntry, TblJournalEntry, AccountSubLedger
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from api.serializers.accounting import JournalEntryModelSerializer, AccountLedgerSerializer
from django.shortcuts import get_object_or_404

@api_view(['PUT'])
def update_account_type(request, pk):
    ac = get_object_or_404(AccountChart, pk=pk)
    ac.account_type=request.query_params.get('accountType')
    ac.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_ledger(request, pk):
    subledger = get_object_or_404(AccountLedger, pk=pk)
    subledger.ledger_name = request.data.get('content', subledger.ledger_name)
    subledger.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_group(request, pk):
    ledger = get_object_or_404(AccountChart, pk=pk)
    ledger.group = request.data.get('content', ledger.group)
    ledger.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_subledger(request, pk):
    sub_ledger = get_object_or_404(AccountSubLedger, pk=pk)
    sub_ledger.sub_ledger_name = request.data.get('content', sub_ledger.sub_ledger_name)
    sub_ledger.save()
    return Response({'Message': 'Successful'})


class ChartOfAccountAPIView(APIView):
    def get(self, request):
        account_chart = AccountChart.objects.all()
        data = {}
        for ac in account_chart:
            if ac.account_type not in data:
                data[ac.account_type] = {"groups":[]}
            data[ac.account_type]["groups"].append({"group_name":ac.group, "ledgers":[]})
            for ledger in ac.accountledger_set.all():
                data[ac.account_type]["groups"][-1]['ledgers'].append({"name":ledger.ledger_name, "total_value":ledger.total_value})
        return Response(data)
    

class JournalEntryAPIView(ListAPIView):
    queryset = TblJournalEntry.objects.all()
    serializer_class = JournalEntryModelSerializer


class TrialBalanceAPIView(APIView):

    def get(self, request):
        trial_balance = []
        total = {'debit_total':0, 'credit_total':0}
        ledgers = AccountLedger.objects.filter(total_value__gt=0)
        for led in ledgers:
            data = {}
            data['account']=led.ledger_name
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
        trial_balance = sorted(trial_balance, key=lambda x:x['account_head'])
        context = {
            'trial_balance': trial_balance,
            "total": total
        }
        print(context)
        return Response(context)


class ProfitAndLossAPIView(APIView):

    def get(self, request):
        expense = AccountLedger.objects.filter(account_chart__account_type="Expense")
        income = AccountLedger.objects.filter(account_chart__account_type="Revenue")
        expense_serializer = AccountLedgerSerializer(expense, many=True)
        income_serializer = AccountLedgerSerializer(income, many=True)
        total_income, total_expense = 0, 0

        for income in income_serializer.data:
            total_income += float(income['total_value'])
        
        for expense in expense_serializer.data:
            total_expense += float(expense['total_value'])

        data = {
            "income":income_serializer.data,
            "expense": expense_serializer.data,
            "total_income": total_income,
            "total_expense":total_expense
        }
        return Response(data)
    

class BalanceSheetAPIView(APIView):

    def get(self, request):
        
        return Response({})

