# Generated by Django 4.0.6 on 2023-07-05 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_branchstocktracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='productmultiprice',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
