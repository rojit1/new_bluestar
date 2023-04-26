# Generated by Django 4.0.6 on 2023-04-24 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='depreciation',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.assetpurchaseitem'),
        ),
        migrations.AddField(
            model_name='accountsubledger',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.accountledger'),
        ),
        migrations.AddField(
            model_name='accountledger',
            name='account_chart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.accountchart'),
        ),
    ]
