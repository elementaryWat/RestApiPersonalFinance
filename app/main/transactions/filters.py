from django_filters import FilterSet, DateRangeFilter, DateFilter
from core.models import Transaction


class CustomTransactionFilter(FilterSet):
    date_gte = DateFilter(
        field_name='transaction_date', lookup_expr=('gte'))
    date_gt = DateFilter(field_name='transaction_date', lookup_expr=('gt'))
    date_lt = DateFilter(field_name='transaction_date', lookup_expr=('lt'))
    date_lte = DateFilter(
        field_name='transaction_date', lookup_expr=('lte'))
    date_range = DateRangeFilter(field_name='transaction_date')

    class Meta:
        model = Transaction
        fields = {
            'paid': ['exact'],
            'category': ['exact'],
            'account': ['exact'],
        }
