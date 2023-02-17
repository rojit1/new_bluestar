# Generated by Django 4.0.6 on 2022-07-30 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_branch'),
        ('bill', '0003_alter_bill_payment_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.organization'),
        ),
    ]