from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model


from django.db import models
from django.dispatch import receiver
from organization.models import Organization
from product.models import Product, ProductStock
from root.utils import BaseModel
from django.db.models.signals import post_save
from .utils import product_sold


User = get_user_model()


class TblTaxEntry(models.Model):
    idtbltaxEntry = models.AutoField(primary_key=True)
    fiscal_year = models.CharField(max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    bill_date = models.DateField(null=True)
    amount = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    taxable_amount = models.FloatField(null=True)
    tax_amount = models.FloatField(null=True)
    is_printed = models.CharField(max_length=20, default="Yes")
    is_active = models.CharField(max_length=20, default="Yes")
    printed_time = models.CharField(null=True, max_length=20)
    entered_by = models.CharField(null=True, max_length=20)
    printed_by = models.CharField(null=True, max_length=20)
    is_realtime = models.CharField(max_length=20, default="Yes")
    sync_with_ird = models.CharField(max_length=20, default="Yes")
    payment_method = models.CharField(null=True, max_length=20, default="Cash")
    vat_refund_amount = models.FloatField(default=0.0)
    transaction_id = models.CharField(null=True, max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tbltaxentry"

    def __str__(self):
        return f"{self.idtbltaxEntry}- {self.fiscal_year} - {self.bill_no}"


class TblSalesEntry(models.Model):
    tblSalesEntry = models.AutoField(primary_key=True)
    bill_date = models.CharField(null=True, max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=True, default=0.0)
    NoTaxSales = models.FloatField(default=0.0)
    ZeroTaxSales = models.FloatField(default=0.0)
    taxable_amount = models.FloatField(null=True, default=0.0)
    tax_amount = models.FloatField(null=True, default=0.0)
    miti = models.CharField(null=True, max_length=20)
    ServicedItem = models.CharField(max_length=20, default="Goods")
    quantity = models.PositiveIntegerField(default=1)
    exemptedSales = models.CharField(default="0", max_length=20)
    export = models.CharField(default="0", max_length=20)
    exportCountry = models.CharField(default="0", max_length=20)
    exportNumber = models.CharField(default="0", max_length=20)
    exportDate = models.CharField(default="0", max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tblSalesEntry"

    def __str__(self):
        return f"{self.tblSalesEntry}- {self.bill_date} - {self.bill_no}"


class TablReturnEntry(models.Model):
    idtblreturnEntry = models.AutoField(primary_key=True)
    bill_date = models.CharField(null=True, max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    amount = models.FloatField(null=True, default=0.0)
    NoTaxSales = models.FloatField(default=0.0)
    ZeroTaxSales = models.FloatField(default=0.0)
    taxable_amount = models.FloatField(null=True, default=0.0)
    tax_amount = models.FloatField(null=True, default=0.0)
    miti = models.CharField(null=True, max_length=20)
    ServicedItem = models.CharField(max_length=20, default="Goods")
    quantity = models.PositiveIntegerField(default=1)
    reason = models.TextField(null=True, blank=True)
    exemptedSales = models.CharField(default="0", max_length=20)
    export = models.CharField(default="0", max_length=20)
    exportCountry = models.CharField(default="0", max_length=20)
    exportNumber = models.CharField(default="0", max_length=20)
    exportDate = models.CharField(default="0", max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tblreturnentry"

    def __str__(self):
        return f"{self.idtblreturnEntry}- {self.bill_date} - {self.bill_no}"


class PaymentType(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Payment Type Title")
    description = models.TextField(null=True, verbose_name="Payment Type Description")
    icon = models.ImageField(upload_to="payment-type/icons/", null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name="Payment Type Slug")

    def __str__(self):
        return self.title


class BillItem(BaseModel):
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(
        max_length=255, verbose_name="Product Title", null=True
    )
    product_quantity = models.PositiveBigIntegerField(default=1)
    rate = models.FloatField(default=0.0)
    unit_title = models.CharField(max_length=50, null=True)
    amount = models.FloatField(
        default=0.0,
    )
    is_taxable = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product_title}"


''' Signal for Decresing Product Stock after Sold '''

def update_stock(sender, instance, **kwargs):
    stock = ProductStock.objects.get(product=instance.product)
    try:
        stock.stock_quantity = stock.stock_quantity - int(instance.product_quantity)
        stock.save()
    except Exception as e:
        print(e)
    product_sold(instance=instance)
    

post_save.connect(update_stock, sender=BillItem)

""" **************************************** """

class Bill(BaseModel):
    fiscal_year = models.CharField(max_length=20)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    agent_name = models.CharField(max_length=255, null=True)
    terminal = models.CharField(max_length=10, default="1")
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_address = models.CharField(max_length=255, null=True, blank=True)
    customer_tax_number = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey("user.Customer", on_delete=models.SET_NULL, null=True)
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField(auto_now_add=True)

    transaction_miti = models.CharField(max_length=255, null=True, blank=True)
    sub_total = models.FloatField(default=0.0)
    discount_amount = models.FloatField(default=0.0)
    taxable_amount = models.FloatField(default=0.0)
    tax_amount = models.FloatField(default=0.0)
    grand_total = models.FloatField(default=0.0)
    service_charge = models.FloatField(default=0.0)

    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    amount_in_words = models.TextField(null=True, blank=True)
    payment_mode = models.CharField(
        max_length=255, default="Cash", blank=True, null=True
    )

    bill_items = models.ManyToManyField(BillItem, blank=False)
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.SET_NULL, null=True
    )
    branch = models.ForeignKey(
        "organization.Branch", on_delete=models.SET_NULL, null=True
    )
    print_count = models.PositiveIntegerField(default=1)
    # is_taxable = models.BooleanField(default=True)
    bill_count_number = models.PositiveIntegerField(blank=True, null=True, db_index=True)   

    class Meta:
        unique_together = 'invoice_number', 'fiscal_year', 'branch'

    def __str__(self):
        return f"{self.customer_name}-{self.transaction_date}- {self.grand_total}"

from .utils import create_journal_for_bill

@receiver(post_save, sender=Bill)
def create_invoice_number(sender, instance, created, **kwargs):
    current_fiscal_year = Organization.objects.last().current_fiscal_year

    if created and not instance.payment_mode.lower() == "complimentary":
        """
        Accounting Section to create Journals after Bill Create
        """
        try:
            create_journal_for_bill(instance)
        except Exception as e:
            pass
        # ___________________________________

        branch = instance.branch.branch_code
        terminal = instance.terminal

        bill_number = 0 
        invoice_number = ""
        instance.fiscal_year = current_fiscal_year
        if terminal == 1:
            last_bill = Bill.objects.filter(terminal=terminal, fiscal_year = current_fiscal_year, branch=instance.branch).order_by('-bill_count_number').first()
            if not last_bill:
                bill_number = 1
            else:
                bill_number = last_bill.bill_count_number + 1

            if branch is not None:
                invoice_number = f"{branch}-{terminal}-{bill_number}"
            else:
                invoice_number = f"{terminal}-{bill_number}"
            
            instance.invoice_number = invoice_number
            instance.bill_count_number=bill_number
        else:
            invoice_number = instance.invoice_number

        a = TblTaxEntry(
            fiscal_year=current_fiscal_year,
            bill_no=invoice_number,
            customer_name=instance.customer_name,
            customer_pan=instance.customer_tax_number,
            bill_date=instance.transaction_date,
            amount=instance.grand_total,
            taxable_amount=instance.taxable_amount,
            tax_amount=instance.tax_amount,
            is_printed="Yes",
            printed_time=str(datetime.now().time().strftime(("%I:%M %p"))),
            entered_by=instance.agent_name,
            printed_by=instance.agent_name,
            is_realtime="Yes",
            sync_with_ird="Yes",
            payment_method=instance.payment_mode,
            vat_refund_amount=0.0,
            transaction_id="-",
        )

        b = TblSalesEntry(
            bill_date=instance.transaction_date,
            customer_name=instance.customer_name,
            customer_pan=instance.customer_tax_number,
            amount=instance.grand_total,
            NoTaxSales=0.0,
            ZeroTaxSales=0.0,
            taxable_amount=instance.taxable_amount,
            tax_amount=instance.tax_amount,
            miti=instance.transaction_miti,
            ServicedItem="Goods",
            quantity=1.0,
            bill_no=invoice_number,
        )

        if instance.tax_amount == 0:
            a.exemptedSales = instance.sub_total
            b.exemptedSales = instance.sub_total

        b.save()

        a.save()
        instance.save()


class BillPayment(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT)
    payment_mode = models.CharField(max_length=100)
    rrn = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.payment_mode
    
class ConflictBillNumber(BaseModel):
    invoice_number = models.CharField(max_length=50)

    def __str__(self):
        return self.invoice_number
