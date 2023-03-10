# Generated by Django 4.0.6 on 2023-02-24 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_type', models.CharField(max_length=100)),
                ('ledger', models.CharField(max_length=100, unique=True)),
                ('financial_statement', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccountLedger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sub_ledger_name', models.CharField(max_length=200, unique=True)),
                ('total_value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('affects_cash_flow', models.CharField(max_length=20)),
                ('account_chart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.accountchart')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
