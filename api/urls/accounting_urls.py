from ..views.accounting import update_account_type ,update_account_group, update_account_ledger

from django.urls import path

urlpatterns = [
    path("update-account-type/<int:pk>/", update_account_type, name="update_account_type"),
    path("update-account-group/<int:pk>/", update_account_group, name="update_account_group"),
    path("update-account-ledger/<int:pk>/", update_account_ledger, name="update_account_ledger"),

]
