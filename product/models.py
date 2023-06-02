from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from root.utils import BaseModel
from user.models import Customer
from organization.models import Branch


class ProductCategory(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Category Title", unique=True)
    slug = models.SlugField(verbose_name="Category Slug", null=True)
    description = models.TextField(
        verbose_name="Category Description", null=True, blank=True
    )

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Product Name", unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Product Slug", null=True)
    description = models.TextField(
        null=True, blank=True, verbose_name="Product Description"
    )
    unit = models.CharField(null=True, max_length=100, blank=True)
    
    is_taxable = models.BooleanField(default=True)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to="product/images/", null=True, blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_id = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(null=True, max_length=100, blank=True)
    reconcile = models.BooleanField(default=False)
    is_billing_item = models.BooleanField(default=True)
    is_produced = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.title} - {self.category.title}"


class ProductStock(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    stock_quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.product.title} -> {self.stock_quantity}'


''' Signal to create ProductStock after Product instance is created '''


def create_stock(sender, instance, **kwargs):
    try:
        ProductStock.objects.create(product=instance)
    except Exception as e:
        print(e)

post_save.connect(create_stock, sender=Product)


"""      ***********************       """




from django.contrib.auth import get_user_model

User = get_user_model()

class ProductMultiprice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.FloatField()
    
    def __str__(self):
        return f"{self.product} - {self.product_price}"



class CustomerProduct(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.FloatField(default=0.0)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.title} - Rs. {self.price}"

class BranchStockTracking(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateField()
    opening = models.IntegerField(default=0)
    received = models.IntegerField(default=0)
    wastage = models.IntegerField(default=0)
    returned = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    closing = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)
    discrepancy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.title}"
    
    class Meta:
        unique_together = "branch", "product", "date"


class BranchStock(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.title} to {self.branch.name}'
    
    def save(self, *args, **kwargs):
        if ProductStock.objects.filter(product=self.product).exists():
            product = ProductStock.objects.get(product=self.product)
            product.stock_quantity -= self.quantity
            product.save()
        return super().save(*args, **kwargs)
    

class ItemReconcilationApiItem(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateField()
    wastage = models.IntegerField(default=0)
    returned = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} -> {self.branch.name}"
    
    class Meta:
        unique_together = 'branch', 'product', 'date'