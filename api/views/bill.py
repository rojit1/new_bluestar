from api.serializers.bill import (
    BillDetailSerializer,
    BillItemSerializer,
    PaymentTypeSerializer,
    BillSerializer,
    TablReturnEntrySerializer,
    TblSalesEntrySerializer,
    TblTaxEntrySerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


from bill.models import Bill, PaymentType, TablReturnEntry, TblSalesEntry, TblTaxEntry


class PaymentTypeList(ListAPIView):
    serializer_class = PaymentTypeSerializer
    queryset = PaymentType.objects.active()


class BillInfo(APIView):
    def get(self, request):
        branch_code = self.request.query_params.get("branch_code")
        terminal = self.request.query_params.get("terminal")
        branch_and_terminal = f"{branch_code}-{terminal}"
        if not branch_code or not terminal:
            return Response({"result": "Please enter branch code and terminal"})
        last_bill_number = (
            Bill.objects.filter(invoice_number__startswith=branch_and_terminal)
            .order_by("pk")
            .reverse()
            .first()
        )
        if last_bill_number:
            return Response({"result": last_bill_number.invoice_number})
        return Response({"result": 0})


class BillAPI(ModelViewSet):
    serializer_class = BillSerializer
    queryset = Bill.objects.active()

    def get_queryset(self, *args, **kwargs):
        queryset = Bill.objects.filter(
            is_deleted=False, status=True, agent=self.request.user
        )
        return queryset

    def get_serializer_class(self):
        detail_actions = ["retrieve", "list"]
        if self.action in detail_actions:
            return BillDetailSerializer
        return super().get_serializer_class()


class TblTaxEntryAPI(ModelViewSet):
    pagination_class = None
    serializer_class = TblTaxEntrySerializer
    queryset = TblTaxEntry.objects.all()


class TblSalesEntryAPI(ModelViewSet):
    serializer_class = TblSalesEntrySerializer
    queryset = TblSalesEntry.objects.all()


class TablReturnEntryAPI(ModelViewSet):
    serializer_class = TablReturnEntrySerializer
    queryset = TablReturnEntry.objects.all()
