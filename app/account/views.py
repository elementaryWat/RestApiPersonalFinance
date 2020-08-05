from rest_framework import viewsets, mixins

from account.serializers import AccountTypeSerializer
from core.models import AccountType


class AccountTypeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    # Manage Account Types in the database
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
