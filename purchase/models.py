from django.db import models
from root.utils import BaseModel
from product.models import Product

class Vendor(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


# class ProductPurchase(BaseModel):
#     products = models.ForeignKey(Product, on_delete=models.CASCADE)
#     purchases = models.ForeignKey('Purchase', on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.product.title} purchased X  {self.quantity}'


# class Purchase(BaseModel):
#     vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
#     products = models.ManyToManyField(Product, blank=False, null=False)
#     purchase_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'purchased {self.product.title} from {self.vendor.name}'



    


