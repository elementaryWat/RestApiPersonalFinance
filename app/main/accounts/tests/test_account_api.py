from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Account, AccountType
from main.accounts.serializers import AccountSerializer

ACCOUNTS_URL = reverse('accounts:accounts-list')


class PublicAccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrive_profile_not_authenticated(self):
        # Test authentication is required for retrieve user profile
        res = self.client.get(ACCOUNTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountApiTests(TestCase):
    # Test API requests that require authentication
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testemail@test.com",
            password="test1234"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_account_list(self):
        # Test for showing created accounts
        account_type = AccountType.objects.create(
            name="Account Type", icon_name="icon")
        Account.objects.create(name="Account 1", description="description 1",
                               account_type=account_type, user=self.user)
        Account.objects.create(name="Account 2", description="description 2",
                               account_type=account_type, user=self.user)

        accounts = Account.objects.all().order_by('-name')
        serialized_accounts = AccountSerializer(accounts, many=True)
        res = self.client.get(ACCOUNTS_URL)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_accounts.data)

    def test_retrieve_account_list_limited_to_user(self):
        # Test for showing created accounts for the logged in user
        another_user = get_user_model().objects.create_user(
            email="another@test.com",
            password="test1234"
        )
        account_type = AccountType.objects.create(
            name="Account Type", icon_name="icon")
        account1 = Account.objects.create(name="Account 1", description="description 1",
                                          account_type=account_type, user=self.user)
        Account.objects.create(name="Account 2", description="description 2",
                               account_type=account_type, user=another_user)

        res = self.client.get(ACCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], account1.name)
