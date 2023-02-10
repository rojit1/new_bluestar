
from django.urls import path
urlpatterns = []

from .views import ProductCategoryList,ProductCategoryDetail,ProductCategoryCreate,ProductCategoryUpdate,ProductCategoryDelete
urlpatterns += [
path('prdct/category/', ProductCategoryList.as_view(), name='product_category_list'),
path('prdct/category/<int:pk>/', ProductCategoryDetail.as_view(), name='product_category_detail'),
path('prdct/category/create/', ProductCategoryCreate.as_view(), name='product_category_create'),
path('prdct/category/<int:pk>/update/', ProductCategoryUpdate.as_view(), name='product_category_update'),
path('prdct/category/delete', ProductCategoryDelete.as_view(), name='product_category_delete'),
]
               
from .views import ProductList,ProductDetail,ProductCreate,ProductUpdate,ProductDelete
urlpatterns += [
path('product/', ProductList.as_view(), name='product_list'),
path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
path('product/create/', ProductCreate.as_view(), name='product_create'),
path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
path('product/delete', ProductDelete.as_view(), name='product_delete'),
]
               
from .views import CustomerProductList,CustomerProductDetail,CustomerProductCreate,CustomerProductUpdate,CustomerProductDelete
urlpatterns += [
path('prdct/client/', CustomerProductList.as_view(), name='customerproduct_list'),
path('prdct/client/<int:pk>/', CustomerProductDetail.as_view(), name='customerproduct_detail'),
path('prdct/client/create/', CustomerProductCreate.as_view(), name='customerproduct_create'),
path('prdct/client/<int:pk>/update/', CustomerProductUpdate.as_view(), name='customerproduct_update'),
path('prdct/client/delete', CustomerProductDelete.as_view(), name='customerproduct_delete'),
]
               