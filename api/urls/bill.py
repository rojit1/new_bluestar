from api.views.bill import (
    BillInfo,
    PaymentTypeList,
    BillAPI,
    TblTaxEntryAPI,
    TblSalesEntryAPI,
    TablReturnEntryAPI,
)
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

router.register("bill", BillAPI)
router.register("tax-entry", TblTaxEntryAPI)
router.register("sales-entry", TblSalesEntryAPI)
router.register("return-entry", TablReturnEntryAPI)

urlpatterns = [
    path("payment-list/", PaymentTypeList.as_view(), name="api_payment_type_list"),
    path("bill-info/", BillInfo.as_view(), name="api_bill_info"),
] + router.urls
