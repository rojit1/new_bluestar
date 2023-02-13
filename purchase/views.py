from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,UpdateView,View, TemplateView
from root.utils import DeleteMixin
from .models import Vendor, ProductPurchase
from .forms import VendorForm, ProductPurchaseForm
from django.shortcuts import render, redirect


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

'''  -------------------------------------    '''

class ProductPurchaseCreateView(CreateView):
    model = ProductPurchase
    form_class = ProductPurchaseForm
    template_name = "purchase/purchase_create.html"

    def form_valid(self, form):
        form_data = form.data
        print(form_data)

        product_ids =  form_data.get('product_id_list', '')
        product_quantity = dict()

        if product_ids:
            product_ids = product_ids.split(',')
        else:
            pass

        for id in product_ids:
            pid = 'id_bill_item_quantity_'+str(id)
            product_quantity[str(id)] = form_data.get(pid)
            
        print(product_quantity)


        return redirect('/purchase/create/' )
    



class ProductPurchaseListView(TemplateView):
    template_name = 'purchase/purchase_list.html'


