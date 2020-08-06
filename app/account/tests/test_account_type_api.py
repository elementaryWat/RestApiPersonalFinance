from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import AccountType
from account.serializers import AccountTypeSerializer

ACCOUNT_TYPE_URL = reverse('account:accounttype-list')


class PublicAccountTypeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_account_type_list(self):
        # Test for showing created accounts
        AccountType.objects.create(name="Account Type 1", icon_name="icon 1")
        AccountType.objects.create(name="Account Type 2", icon_name="icon 2")

        res = self.client.get(ACCOUNT_TYPE_URL)

        account_types = AccountType.objects.all()
        serialized_account_types = AccountTypeSerializer(
            account_types, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_account_types.data)
