from django.urls import path
from .views import AccountChartList,AccountChartDetail,AccountChartCreate,AccountChartUpdate,AccountChartDelete

urlpatterns = [
path('accountchart/', AccountChartList.as_view(), name='accountchart_list'),
path('accountchart/<int:pk>/', AccountChartDetail.as_view(), name='accountchart_detail'),
path('accountchart/create/', AccountChartCreate.as_view(), name='accountchart_create'),
path('accountchart/<int:pk>/update/', AccountChartUpdate.as_view(), name='accountchart_update'),
path('accountchart/delete', AccountChartDelete.as_view(), name='accountchart_delete'),
]
 