from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,UpdateView,View
from root.utils import DeleteMixin
from .models import Vendor
from .forms import VendorForm

class VendorMixin:
    model = Vendor
    form_class = VendorForm
    paginate_by = 10
    queryset = Vendor.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('vendor_list')


class VendorList(VendorMixin, ListView):
    template_name = "vendor/vendor_list.html"
    queryset = Vendor.objects.filter(status=True,is_deleted=False)


class VendorDetail(VendorMixin, DetailView):
    template_name = "vendor/vendor_detail.html"


class VendorCreate(VendorMixin, CreateView):
    template_name = "create.html"


class VendorUpdate(VendorMixin, UpdateView):
    template_name = "update.html"


class VendorDelete(VendorMixin, DeleteMixin, View):
    pass
