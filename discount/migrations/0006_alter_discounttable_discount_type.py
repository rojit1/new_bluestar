# Generated by Django 4.0.6 on 2023-02-08 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0005_rename_dicount_type_discounttable_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discounttable',
            name='discount_type',
            field=models.CharField(choices=[('PCT', 'PCT'), ('FLAT', 'FLAT')], max_length=200),
        ),
    ]