# Generated by Django 4.0.6 on 2023-02-27 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountLedger',
            new_name='AccountSubLedger',
        ),
    ]