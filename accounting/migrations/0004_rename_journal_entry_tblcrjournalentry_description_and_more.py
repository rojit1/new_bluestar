# Generated by Django 4.0.6 on 2023-02-27 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_tbljournalentry_tbldrjournalentry_tblcrjournalentry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblcrjournalentry',
            old_name='journal_entry',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='tbldrjournalentry',
            old_name='journal_entry',
            new_name='description',
        ),
    ]
