# Generated by Django 4.0.6 on 2023-02-16 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_purchase_discount_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblpurchaseEntry',
            fields=[
                ('idtblpurchaseEntry', models.BigAutoField(primary_key=True, serialize=False)),
                ('bill_date', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_no', models.IntegerField(blank=True, null=True)),
                ('pp_no', models.CharField(blank=True, max_length=20, null=True)),
                ('buyer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('buyer_pan', models.CharField(blank=True, max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('no_tax_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('purchase_req_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tblpurchaseEntry',
            },
        ),
        migrations.CreateModel(
            name='TblpurchaseReturn',
            fields=[
                ('idtblpurchaseEntry', models.BigAutoField(primary_key=True, serialize=False)),
                ('bill_date', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_no', models.IntegerField(blank=True, null=True)),
                ('pp_no', models.CharField(blank=True, max_length=20, null=True)),
                ('buyer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('buyer_pan', models.CharField(blank=True, max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tax_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('no_tax_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('purchase_req_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tblpurchaseReturn',
            },
        ),
    ]
