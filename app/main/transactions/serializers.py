from rest_framework import serializers
from core.models import Transaction
from main.categories.serializers import TransactionCategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'description', 'paid',
                  'date_created', 'category', 'account',)
        read_only_fields = ('id', )
