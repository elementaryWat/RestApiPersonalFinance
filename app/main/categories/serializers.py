from rest_framework import serializers
from core.models import TransactionCategory
# from core.serializers import FilteredListSerializerByUser


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        # TODO: Add filter by logged user
        # list_serializer_class = FilteredListSerializerByUser
        fields = ('id', 'name', 'icon_name', 'color', 'category_type', 'user',)
        read_only_fields = ('id', 'user')
