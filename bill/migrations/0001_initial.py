# Generated by Django 4.0.6 on 2022-07-23 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_product_unit'),
        ('user', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, verbose_name='Payment Type Title')),
                ('description', models.TextField(null=True, verbose_name='Payment Type Description')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='payment-type/icons/')),
                ('slug', models.SlugField(unique=True, verbose_name='Payment Type Slug')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('product_title', models.CharField(max_length=255, null=True, verbose_name='Product Title')),
                ('product_quantity', models.PositiveBigIntegerField(default=1)),
                ('rate', models.FloatField(default=0.0)),
                ('unit_title', models.CharField(max_length=50, null=True)),
                ('amount', models.FloatField(default=0.0)),
                ('is_taxable', models.BooleanField(default=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_address', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_tax_number', models.CharField(blank=True, max_length=255, null=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_miti', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_total', models.FloatField(default=0.0)),
                ('discount_amount', models.FloatField(default=0.0)),
                ('taxable_amount', models.FloatField(default=0.0)),
                ('tax_amount', models.FloatField(default=0.0)),
                ('grand_total', models.FloatField(default=0.0)),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_in_words', models.TextField(blank=True, null=True)),
                ('bill_items', models.ManyToManyField(to='bill.billitem')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.customer')),
                ('payment_mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bill.paymenttype')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
