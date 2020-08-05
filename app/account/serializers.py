from rest_framework import serializers
from core.models import AccountType


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ('id', 'name', 'icon_name')
        read_only_fields = ('id', )
