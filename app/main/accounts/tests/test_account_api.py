from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Account, AccountType
from main.accounts.serializers import AccountSerializer

ACCOUNTS_URL = reverse('accounts:accounts-list')


def create_sample_account_type(payload={'name': 'account_testing', 'icon_name': 'testing'}):
    return AccountType.objects.create(
        **payload
    )


def get_sample_user(email="sample_user@email.com", password="sample_password"):
    # Create a sample user
    return get_user_model().objects.create_user(email, password)


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
        account_type = create_sample_account_type()
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
        another_user = get_sample_user()
        account_type = create_sample_account_type()
        account1 = Account.objects.create(name="Account 1", description="description 1",
                                          account_type=account_type, user=self.user)
        Account.objects.create(name="Account 2", description="description 2",
                               account_type=account_type, user=another_user)

        res = self.client.get(ACCOUNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], account1.name)

    def test_create_valid_account_success(self):
        # Test creating account with valid payload is successful
        account_type = create_sample_account_type()
        payload = {
            'name': "Account 1",
            'description': "description 1",
            'account_type': account_type.id,
        }
        res = self.client.post(ACCOUNTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_not_create_account_with_empty_data(self):
        # Test not creating a category when the data is empty
        payload = {
            'name': "",
            'description': "",
            'account_type': "",
        }

        res = self.client.post(ACCOUNTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_account_with_wrong_account_type(self):
        # Test not creating a category when the data is empty
        WRONG_ACCOUNT_TYPE_ID = 5
        payload = {
            'name': "Account 1",
            'description': "description 1",
            'account_type': WRONG_ACCOUNT_TYPE_ID,
        }

        res = self.client.post(ACCOUNTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
