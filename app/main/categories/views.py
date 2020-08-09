from rest_framework import viewsets, mixins

from main.categories.serializers import TransactionCategorySerializer
from core.models import TransactionCategory
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TransactionCategoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Return objects for the current authenticated user only
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Adds the user logged in to the category
        serializer.save(user=self.request.user)
