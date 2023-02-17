# Generated by Django 4.0.6 on 2022-08-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0015_bill_transaction_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablreturnentry',
            name='amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='tablreturnentry',
            name='tax_amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='tablreturnentry',
            name='taxable_amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='tblsalesentry',
            name='amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='tblsalesentry',
            name='tax_amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='tblsalesentry',
            name='taxable_amount',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]