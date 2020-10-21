from rest_framework import viewsets

from .serializers import TransactionSerializer
from core.models import Transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .filters import CustomTransactionFilter


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_class = CustomTransactionFilter

    def get_queryset(self):
        # Return objects for the current authenticated user only
        return self.queryset.filter(category__user=self.request.user)

    # def perform_create(self, serializer):
    #     # Adds the user logged in to the category
    #     serializer.save(user=self.request.user)
