# Generated by Django 4.0.6 on 2022-08-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0009_alter_tablreturnentry_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='agent_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='fiscal_year',
            field=models.CharField(max_length=20, null=True),
        ),
    ]