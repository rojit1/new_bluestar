from django.urls import path

from .views import VendorList,VendorDetail,VendorCreate,VendorUpdate,VendorDelete

urlpatterns = [
    path('vendor/', VendorList.as_view(), name='vendor_list'),
    path('vendor/<int:pk>/', VendorDetail.as_view(), name='vendor_detail'),
    path('vendor/create/', VendorCreate.as_view(), name='vendor_create'),
    path('vendor/<int:pk>/update/', VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/delete', VendorDelete.as_view(), name='vendor_delete'),
]