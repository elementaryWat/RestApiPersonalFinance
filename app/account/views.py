from rest_framework import viewsets, mixins

from account.serializers import AccountTypeSerializer, AccountSerializer
from core.models import AccountType, Account
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AccountTypeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
