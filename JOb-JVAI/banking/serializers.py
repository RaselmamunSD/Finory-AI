"""
Banking module serializers
"""
from rest_framework import serializers
from .models import BankAccount, BankTransaction


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
