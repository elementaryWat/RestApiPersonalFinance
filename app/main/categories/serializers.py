from rest_framework import serializers
from core.models import TransactionCategory


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ('id', 'name', 'icon_name', 'category_type', 'user',)
        read_only_fields = ('id', 'user')
