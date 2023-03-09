
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from accounting.models import AccountChart, AccountSubLedger

@api_view(['PUT'])
def update_account_type(request, pk):
    ac = AccountChart.objects.get(pk=pk)
    ac.account_type=request.query_params.get('accountType')
    ac.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_sub_ledger(request, pk):
    subledger = AccountSubLedger.objects.get(pk=pk)
    subledger.sub_ledger_name = request.data.get('content', subledger.sub_ledger_name)
    subledger.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_ledger(request, pk):
    ledger = AccountChart.objects.get(pk=pk)
    ledger.ledger = request.data.get('content', ledger.ledger)
    ledger.save()
    return Response({'Message': 'Successful'})