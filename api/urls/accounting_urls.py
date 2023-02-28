from ..views.accounting import update_account_type 
from django.urls import path

urlpatterns = [
    path("update-account-type/<int:pk>/", update_account_type, name="update_account_type")
]
