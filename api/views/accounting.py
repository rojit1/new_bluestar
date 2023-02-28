
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from accounting.models import AccountChart

@api_view(['PUT'])
def update_account_type(request, pk):
    ac = AccountChart.objects.get(pk=pk)
    ac.account_type=request.query_params.get('accountType')
    ac.save()
    return Response({'Message': 'Successful'})
