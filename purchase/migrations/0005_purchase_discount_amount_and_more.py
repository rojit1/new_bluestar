# Generated by Django 4.0.6 on 2023-02-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_rename_price_productpurchase_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='discount_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='discount_percentage',
            field=models.IntegerField(default=0),
        ),
    ]