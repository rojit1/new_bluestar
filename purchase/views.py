from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,UpdateView,View, TemplateView
from root.utils import DeleteMixin
from .models import Vendor, ProductPurchase, Purchase, TblpurchaseEntry
from .forms import VendorForm, ProductPurchaseForm
from django.shortcuts import render, redirect
from product.models import Product


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
        bill_no = form_data.get('bill_no', None)
        bill_date = form_data.get('bill_date', None)
        pp_no = form_data.get('pp_no',None)
        vendor_id = form_data.get('vendor')
        sub_total = form_data.get('sub_total')
        discount_percentage = form_data.get('discount_percentage')
        discount_amount = form_data.get('discount_amount')
        taxable_amount = form_data.get('taxable_amount')
        non_taxable_amount = form_data.get('non_taxable_amount')
        tax_amount = form_data.get('tax_amount')
        grand_total = form_data.get('grand_total')
        amount_in_words = form_data.get('amount_in_words')
        payment_mode = form_data.get('payment_mode')


        purchase_object = Purchase(
            vendor_id=vendor_id,sub_total=sub_total, bill_date=bill_date,
            discount_percentage=discount_percentage,discount_amount=discount_amount,
            taxable_amount=taxable_amount, non_taxable_amount=non_taxable_amount,
            tax_amount=tax_amount, grand_total=grand_total,
            amount_in_words=amount_in_words, payment_mode=payment_mode
        )
        purchase_object.save()
        product_ids =  form_data.get('product_id_list', '')

        item_name = ''
        total_quantity = 0
        buyer = Vendor.objects.get(pk=vendor_id)
        buyer_name = buyer.name
        buyer_pan = buyer.pan_no

        if product_ids:
            product_ids = product_ids.split(',')

        for id in product_ids:
            id = int(id)
            quantity = int(form_data.get(f'id_bill_item_quantity_{id}'))
            total_quantity += quantity
            item_name += Product.objects.get(pk=id).title +'-'+ str(quantity) + ', '
            rate = float(form_data.get(f'id_bill_item_rate_{id}'))
            item_total = quantity * rate
            ProductPurchase.objects.create(product_id=id, purchase=purchase_object, quantity=quantity, rate=rate, item_total=item_total)

        TblpurchaseEntry.objects.create(
            bill_no=bill_no, bill_date=bill_date, pp_no=pp_no, buyer_name=buyer_name, buyer_pan=buyer_pan,
            item_name=item_name, quantity=total_quantity, amount=grand_total, tax_amount=tax_amount, non_tax_purchase=non_taxable_amount
        )

        return redirect('/purchase/create/' )
    


class PurchaseListView(ListView):
    model = Purchase
    queryset = Purchase.objects.filter(is_deleted=False)
    template_name = 'purchase/purchase_list.html'

class PurchaseDetailView(TemplateView):
    template_name = 'purchase/purchase_detail.html'



