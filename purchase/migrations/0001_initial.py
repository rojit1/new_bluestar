# Generated by Django 4.0.6 on 2023-02-20 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('quantity', models.IntegerField()),
                ('item_total', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TblpurchaseEntry',
            fields=[
                ('idtblpurchaseEntry', models.BigAutoField(primary_key=True, serialize=False)),
                ('bill_date', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_no', models.CharField(blank=True, max_length=30, null=True)),
                ('pp_no', models.CharField(blank=True, max_length=20, null=True)),
                ('vendor_name', models.CharField(blank=True, max_length=200, null=True)),
                ('vendor_pan', models.CharField(blank=True, max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('non_tax_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('purchase_req_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tblpurchaseEntry',
            },
        ),
        migrations.CreateModel(
            name='TblpurchaseReturn',
            fields=[
                ('idtblpurchaseReturn', models.BigAutoField(primary_key=True, serialize=False)),
                ('bill_date', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_no', models.CharField(blank=True, max_length=30, null=True)),
                ('pp_no', models.CharField(blank=True, max_length=20, null=True)),
                ('vendor_name', models.CharField(blank=True, max_length=200, null=True)),
                ('vendor_pan', models.CharField(blank=True, max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('non_tax_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'tblpurchaseReturn',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=10, null=True)),
                ('pan_no', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('bill_date', models.DateField(blank=True, max_length=50, null=True)),
                ('bill_no', models.CharField(blank=True, max_length=30, null=True)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=9)),
                ('discount_percentage', models.IntegerField(default=0)),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=9)),
                ('taxable_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('non_taxable_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('amount_in_words', models.CharField(max_length=255)),
                ('payment_mode', models.CharField(max_length=30)),
                ('products', models.ManyToManyField(through='purchase.ProductPurchase', to='product.product')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.vendor')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='productpurchase',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.purchase'),
        ),
    ]
