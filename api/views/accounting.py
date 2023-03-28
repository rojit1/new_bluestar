
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from accounting.models import AccountChart, AccountLedger

@api_view(['PUT'])
def update_account_type(request, pk):
    ac = AccountChart.objects.get(pk=pk)
    ac.account_type=request.query_params.get('accountType')
    ac.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_ledger(request, pk):
    subledger = AccountLedger.objects.get(pk=pk)
    subledger.ledger_name = request.data.get('content', subledger.ledger_name)
    subledger.save()
    return Response({'Message': 'Successful'})

@api_view(['PUT'])
def update_account_group(request, pk):
    ledger = AccountChart.objects.get(pk=pk)
    ledger.group = request.data.get('content', ledger.group)
    ledger.save()
    return Response({'Message': 'Successful'})