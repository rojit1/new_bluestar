from django.urls import path
from organization.views import IndexView

from .views import (
    OrganizationCreate,
    OrganizationDelete,
    OrganizationDetail,
    OrganizationUpdate,
    StaticPageCreate,
    StaticPageDelete,
    StaticPageDetail,
    StaticPageList,
    StaticPageUpdate,
)


app_name = "org"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]


urlpatterns += [
    path("organization/", OrganizationDetail.as_view(), name="organization_detail"),
    path(
        "organization/create/", OrganizationCreate.as_view(), name="organization_create"
    ),
    path(
        "organization/update/",
        OrganizationUpdate.as_view(),
        name="organization_update",
    ),
    path(
        "organization/delete", OrganizationDelete.as_view(), name="organization_delete"
    ),
]


urlpatterns += [
    path("staticpage/", StaticPageList.as_view(), name="staticpage_list"),
    path("staticpage/<int:pk>/", StaticPageDetail.as_view(), name="staticpage_detail"),
    path("staticpage/create/", StaticPageCreate.as_view(), name="staticpage_create"),
    path(
        "staticpage/<int:pk>/update/",
        StaticPageUpdate.as_view(),
        name="staticpage_update",
    ),
    path("staticpage/delete", StaticPageDelete.as_view(), name="staticpage_delete"),
]

from .views import BranchList,BranchDetail,BranchCreate,BranchUpdate,BranchDelete,reportView, getoutletName
urlpatterns += [
path('branch/', BranchList.as_view(), name='branch_list'),
path('branch/<int:pk>/', BranchDetail.as_view(), name='branch_detail'),
path('branch/create/', BranchCreate.as_view(), name='branch_create'),
path('branch/<int:pk>/update/', BranchUpdate.as_view(), name='branch_update'),
path('branch/delete', BranchDelete.as_view(), name='branch_delete'),
path(r"report/<str:outlet>", reportView, name="report_view"),
path("outletname", getoutletName, name="outlet_name"),
]
               