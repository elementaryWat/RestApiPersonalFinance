from rest_framework import serializers
from core.models import AccountType, Account


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ('id', 'name', 'icon_name')
        read_only_fields = ('id', )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'description', 'account_type', 'user')
        read_only_fields = ('id', )
