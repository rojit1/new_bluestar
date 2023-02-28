from django.urls import path
from .views import AccountChartList,AccountChartDetail,AccountChartCreate,AccountChartUpdate,AccountChartDelete

urlpatterns = [
path('accountchart/', AccountChartList.as_view(), name='accountchart_list'),
path('accountchart/<int:pk>/', AccountChartDetail.as_view(), name='accountchart_detail'),
path('accountchart/create/', AccountChartCreate.as_view(), name='accountchart_create'),
path('accountchart/<int:pk>/update/', AccountChartUpdate.as_view(), name='accountchart_update'),
path('accountchart/delete', AccountChartDelete.as_view(), name='accountchart_delete'),
]

from .views import AccountSubLedgerList,AccountSubLedgerDetail,AccountSubLedgerCreate,AccountSubLedgerUpdate,AccountSubLedgerDelete
urlpatterns += [
path('accountsubledger/', AccountChartList.as_view(), name='accountsubledger_list'),
path('accountsubledger/<int:pk>/', AccountSubLedgerDetail.as_view(), name='accountsubledger_detail'),
path('accountsubledger/create/', AccountSubLedgerCreate.as_view(), name='accountsubledger_create'),
path('accountsubledger/<int:pk>/update/', AccountSubLedgerUpdate.as_view(), name='accountsubledger_update'),
path('accountsubledger/delete', AccountSubLedgerDelete.as_view(), name='accountsubledger_delete'),
]


from .views import JournalEntryView, TrialBalanceView
urlpatterns += [
    path('journal/', JournalEntryView.as_view(), name="journal_create"),
    path('trial-balance/', TrialBalanceView.as_view(), name="trial_balance_view"),

]
