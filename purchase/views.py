from datetime import date
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import CreateView,DetailView,ListView,UpdateView,View
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
import xlwt

from root.utils import DeleteMixin
from product.models import Product
from organization.models import Organization
from product.models import ProductStock
from .forms import VendorForm, ProductPurchaseForm
from .models import Vendor, ProductPurchase, Purchase, TblpurchaseEntry, TblpurchaseReturn

from bill.views import ExportExcelMixin

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
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor_name = vendor.name
        vendor_pan = vendor.pan_no

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
            bill_no=bill_no, bill_date=bill_date, pp_no=pp_no, vendor_name=vendor_name, vendor_pan=vendor_pan,
            item_name=item_name, quantity=total_quantity, amount=grand_total, tax_amount=tax_amount, non_tax_purchase=non_taxable_amount
        )

        return redirect('/purchase/create/' )
    


class PurchaseListView(ListView):
    model = Purchase
    queryset = Purchase.objects.filter(is_deleted=False)
    template_name = 'purchase/purchase_list.html'


class PurchaseDetailView(DetailView):
    template_name = 'purchase/purchase_detail.html'
    queryset = Purchase.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        org = Organization.objects.first()
        context =  super().get_context_data(**kwargs)
        context['organization'] = org
        return context



class MarkPurchaseVoid(View):

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        reason = request.POST.get('voidReason')
        purchase = get_object_or_404(Purchase, pk=id)
        purchase.status = False
        purchase.save()


        purchased_products = purchase.productpurchase_set.all()
        for item in purchased_products:
            stock = ProductStock.objects.get(product=item.product)
            stock.stock_quantity = stock.stock_quantity-item.quantity
            stock.save()
            

        entry_obj = TblpurchaseEntry.objects.get(pk=id)
        TblpurchaseReturn.objects.create(
            bill_date=entry_obj.bill_date,
            bill_no=entry_obj.bill_no,
            pp_no=entry_obj.pp_no,
            vendor_name=entry_obj.vendor_name,
            vendor_pan=entry_obj.vendor_pan,
            item_name=entry_obj.item_name,
            quantity=entry_obj.quantity,
            unit=entry_obj.unit,
            amount=entry_obj.amount,
            tax_amount=entry_obj.tax_amount,
            non_tax_purchase=entry_obj.non_tax_purchase,
            reason = reason
        )
        
        
        return redirect(
            reverse_lazy("purchase_detail", kwargs={"pk": id})
        )


""" View starting for Purchase Book  """

class PurchaseBookListView(ExportExcelMixin,View):

    def export_to_excel(self, data):
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="purchase_book.xls"'

        common = ['bill_date', "bill_no", "pp_no", "vendor_name", "vendor_pan", "amount", "tax_amount", "non_tax_purchase"]
        common.insert(0, 'idtblpurchaseEntry')
        extra = ["import","importCountry","importNumber", "importDate"]
        

        wb, ws, row_num, font_style_normal, font_style_bold = self.init_xls(
            "Purchase Book", common+extra
        )
        purchase_entry = data.get('purchase_entry')
        rows = purchase_entry.values_list(*common)

        for row in rows:
            row = row + (0,0,0,0)
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style_normal)

        purchase_entry_sum = data.get('purchase_entry_sum')
        print(purchase_entry_sum)

        row_num += 1
        ws.write(row_num, 0, "Total", font_style_normal)
        for key, value in purchase_entry_sum.items():
            key = key.split('__')[0]
            ws.write(row_num, common.index(key), value or 0, font_style_normal)

        common [0] = "idtblpurchaseReturn"
        columns2 = common+extra

        row_num += 1
        ws.write(row_num, 0, "")
        row_num += 1
        ws.write(row_num, 0, "Purchase Return", font_style_bold)
        row_num += 1

        new_columns = ["id"] + columns2[1:]
        for col_num in range(len(columns2)):
            ws.write(row_num, col_num, new_columns[col_num], font_style_bold)

        return_entry = data.get('return_entry')
        rows2 = return_entry.values_list(*common)
        return_entry_sum = data.get('return_entry_sum')

        for row in rows2:
            row = row + (0,0,0,0)
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style_normal)

        row_num += 1
        ws.write(row_num, 0, "Total", font_style_normal)
        for key, value in return_entry_sum.items():
            key = key.split('__')[0]
            ws.write(row_num, common.index(key), value or 0, font_style_normal)


        row_num += 2
        ws.write(row_num, 0, "Grand Total", font_style_bold)

        grand_total = data.get('grand_total')

        for key, value in grand_total.items():
            key = key.split('__')[0]
            ws.write(row_num, common.index(key), value or 0, font_style_bold)
        wb.save(response)
        return response


    def get(self, request, *args, **kwargs):
        today = date.today()
        from_date = request.GET.get('fromDate', today)
        to_date = request.GET.get('toDate', today)
        format = request.GET.get('format', None)

        purchase_entry = TblpurchaseEntry.objects.filter(bill_date__range=[from_date, to_date])
        return_entry = TblpurchaseReturn.objects.filter(bill_date__range=[from_date, to_date])
        purchase_entry_sum = dict()
        return_entry_sum = dict()
        grand_total = dict()

        if purchase_entry and return_entry:
            purchase_entry_sum = purchase_entry.aggregate(Sum('amount'), Sum('tax_amount'), Sum('non_tax_purchase'))
            return_entry_sum = return_entry.aggregate(Sum('amount'), Sum('tax_amount'), Sum('non_tax_purchase'))

            for key in purchase_entry_sum.keys():
                grand_total[key] = purchase_entry_sum[key] - return_entry_sum[key]


        context = {'purchase_entry':purchase_entry, 'return_entry':return_entry,
                    'purchase_entry_sum':purchase_entry_sum, 'return_entry_sum': return_entry_sum, 'grand_total': grand_total}
        
        if format and format =='xls':
            return self.export_to_excel(data=context)


        return render(request, 'purchase/purchase_book.html', context)


"""  ***************   Asset Purchase  ****************  """


from .models import AssetPurchase, Asset, AssetPurchaseItem
from .forms import AssetPurchaseForm
from accounting.models import TblCrJournalEntry, TblDrJournalEntry, TblJournalEntry, AccountSubLedger

class AssetPurchaseMixin:
    model = AssetPurchase
    form_class = AssetPurchaseForm
    paginate_by = 10
    queryset = AssetPurchase.objects.filter(status=True,is_deleted=False)
    success_url = reverse_lazy('assetpurchase_list')

class AssetPurchaseList(AssetPurchaseMixin, ListView):
    template_name = "assetpurchase/assetpurchase_list.html"
    queryset = AssetPurchase.objects.filter(status=True,is_deleted=False)

class AssetPurchaseDetail(AssetPurchaseMixin, DetailView):
    template_name = "assetpurchase/assetpurchase_detail.html"


class AssetPurchaseUpdate(AssetPurchaseMixin, UpdateView):
    template_name = "update.html"

# class AssetPurchaseDelete(AssetPurchaseMixin, DeleteMixin, View):
#     pass

class AssetPurchaseCreate(CreateView):
    model = AssetPurchase
    form_class = AssetPurchaseForm
    template_name = "assetpurchase/assetpurchase_create.html"

    def post(self, request):
        bill_no = request.POST.get('bill_no', None)
        bill_date = request.POST.get('bill_date', None)
        vendor_id = request.POST.get('vendor')
        sub_total = request.POST.get('sub_total')
        discount_percentage = request.POST.get('discount_percentage')
        discount_amount = request.POST.get('discount_amount')
        taxable_amount = request.POST.get('taxable_amount')
        non_taxable_amount = request.POST.get('non_taxable_amount')
        tax_amount = request.POST.get('tax_amount')
        grand_total = request.POST.get('grand_total')
        amount_in_words = request.POST.get('amount_in_words')
        payment_mode = request.POST.get('payment_mode')
        debit_sub_ledger_pk = request.POST.get('sub_ledger')

        asset_purchase = AssetPurchase(
            bill_no=bill_no,
            vendor_id=vendor_id,sub_total=sub_total, bill_date=bill_date,
            discount_percentage=discount_percentage,discount_amount=discount_amount,
            taxable_amount=taxable_amount, non_taxable_amount=non_taxable_amount,
            tax_amount=tax_amount, grand_total=grand_total,
            amount_in_words=amount_in_words, payment_mode=payment_mode
        )
        asset_purchase.save()


        selected_item_list = request.POST.get('select_items_list', [])
        selected_item_list = selected_item_list.split(',')


        for item in selected_item_list:
            if not Asset.objects.filter(title=item).exists():
                asset = Asset.objects.create(title=item)
                quantity = int(request.POST.get(f'id_bill_item_quantity_{item}'))
                rate = float(request.POST.get(f'id_bill_item_rate_{item}'))
                item_total = rate * quantity
                AssetPurchaseItem.objects.create(asset=asset, asset_purchase=asset_purchase, rate=rate, quantity=quantity, item_total=item_total)

            else:
                asset = Asset.objects.get(title=item)
                quantity = int(request.POST.get(f'id_bill_item_quantity_{item}'))
                rate = float(request.POST.get(f'id_bill_item_rate_{item}'))
                item_total = rate * quantity
                AssetPurchaseItem.objects.create(asset=asset, asset_purchase=asset_purchase, rate=rate, quantity=quantity, item_total=item_total)

        # if payment_mode == 'Cash':

        #     try:
        #         credit_sub_ledger = AccountSubLedger.objects.get(sub_ledger_name=payment_mode)
        #         debit_sub_ledger = AccountSubLedger.objects.get(pk=debit_sub_ledger_pk)

        #         journal_entry = TblJournalEntry.objects.create(employee_name=request.user.username)

        #         TblDrJournalEntry.objects.create(sub_ledger=debit_sub_ledger, journal_entry=journal_entry, particulars=f'Debit from bill {bill_no}', debit_amount=grand_total)
        #         credit_sub_ledger.total_value -= grand_total
        #         TblCrJournalEntry.objects.create(sub_ledger=credit_sub_ledger, journal_entry=journal_entry,particulars=f'Cash cr. from bill {bill_no}', credit_amount=grand_total)
        #         debit_sub_ledger.total_value += grand_total
        #     except Exception:
        #         print(Exception)

        return redirect('/')
    


