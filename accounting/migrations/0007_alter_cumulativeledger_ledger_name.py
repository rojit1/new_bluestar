# Generated by Django 4.0.6 on 2023-05-03 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_cumulativeledger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumulativeledger',
            name='ledger_name',
            field=models.CharField(max_length=200),
        ),
    ]
