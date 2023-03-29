from rest_framework import serializers
from accounting.models import TblJournalEntry, TblDrJournalEntry, TblCrJournalEntry, AccountLedger

class DrJournalEntrySerialzier(serializers.ModelSerializer):
    class Meta:
        model = TblDrJournalEntry
        exclude = 'created_at', "updated_at"


class CrJournalEntrySerialzier(serializers.ModelSerializer):
    class Meta:
        model = TblCrJournalEntry
        exclude = 'created_at', "updated_at"


class JournalEntryModelSerializer(serializers.ModelSerializer):
    debit_entries = DrJournalEntrySerialzier(many=True, read_only=True, source="tbldrjournalentry_set")
    credit_entries = CrJournalEntrySerialzier(many=True, read_only=True, source="tblcrjournalentry_set")

    class Meta:
        model = TblJournalEntry
        exclude = 'created_at', "updated_at"

class AccountLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLedger
        fields = "ledger_name", "total_value",
