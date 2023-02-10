from django.db import models
from root.utils import BaseModel
from product.models import Product

class Vendor(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

class Purchase(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product, through='ProductPurchase')
    purchase_date = models.DateField(auto_now=True, blank=True)
    grand_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Purchased from {self.vendor.name} total = {self.grand_amount}'



class ProductPurchase(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()
    item_total = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.product.title} X {self.quantity}'







    


