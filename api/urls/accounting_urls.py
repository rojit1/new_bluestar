from ..views.accounting import update_account_type , update_account_sub_ledger, update_account_ledger

from django.urls import path

urlpatterns = [
    path("update-account-type/<int:pk>/", update_account_type, name="update_account_type"),
    path("update-account-sub-ledger/<int:pk>/", update_account_sub_ledger, name="update_account_sub_ledger"),
    path("update-account-ledger/<int:pk>/", update_account_ledger, name="update_account_ledger"),

]
