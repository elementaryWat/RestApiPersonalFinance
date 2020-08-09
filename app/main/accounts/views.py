from rest_framework import viewsets, mixins

from main.accounts.serializers import AccountTypeSerializer, AccountSerializer
from core.models import AccountType, Account
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AccountTypeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Return objects for the current authenticated user only
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Adds the user logged into the Account
        serializer.save(user=self.request.user)
