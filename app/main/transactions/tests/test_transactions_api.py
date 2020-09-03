from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Transaction, Account, AccountType, TransactionCategory, CATEGORY_TYPES
from main.transactions.serializers import TransactionSerializer
from urllib.parse import urlencode
import datetime

TRANSACTIONS_URL = reverse('transactions:transactions-list')


def url_with_querystring(path, **kwargs):
    return path + '?' + urlencode(kwargs)


def get_transactions_url_with_query_args(**kwargs):
    return url_with_querystring(reverse('transactions:transactions-list'), **kwargs)


def get_detail_transactions_url(transaction):
    return reverse('transactions:transactions-detail', args=(transaction.id,))


class PublicTransactionApiTests(APITestCase):

    def test_retrieve_transactions_profile_not_authenticated(self):
        # Test authentication is required for retrieve user profile
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTransactionApiTests(APITestCase):
    # Test API requests that require authentication
    def setUp(self):
        self.payloadUser = {
            'email': 'username@domain.com', 'password': 'Test1234'}
        self.user = get_user_model().objects.create_user(
            **self.payloadUser
        )

        self.payloadAccountType = {
            'name': 'account_testing', 'icon_name': 'testing'}
        self.accountType = AccountType.objects.create(
            **self.payloadAccountType
        )

        self.payloadAccount = {
            'name': 'Transactions Account',
            'description': 'Some description',
            'account_type': self.accountType,
            'user': self.user
        }
        self.account = Account.objects.create(
            **self.payloadAccount
        )

        self.payloadCategory = {
            'name': 'Salary',
            'icon_name': 'salary icon',
            'category_type': CATEGORY_TYPES.INCOME.value,
            'user': self.user
        }
        self.category = TransactionCategory.objects.create(
            **self.payloadCategory
        )

        self.DATE_TEST = '2020-08-18'
        self.DATE_TODAY = datetime.date.today()
        self.DATES_PREVIOUS_MONTH = ['2020-07-05', '2020-07-16', '2020-07-11']
        self.DATES_THIS_MONTH = ['2020-08-6', '2020-08-17', '2020-08-12']
        self.payloadTransaction = {
            'amount': 200.0,
            'description': 'New transaction',
            'paid': False,
            'transaction_date': self.DATE_TEST,
            'category': self.category,
            'account': self.account
        }
        self.transaction = Transaction.objects.create(
            **self.payloadTransaction
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_transaction_detail(self):
        # Test for retrieving transaction detail

        res = self.client.get(get_detail_transactions_url(self.transaction))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        transaction_serialized = TransactionSerializer(
            Transaction.objects.get(id=self.transaction.id))
        self.assertEqual(transaction_serialized.data, res.data)

    def test_retrieve_transactions_list(self):
        # Test for showing created transactions
        payloadTransaction = {
            'amount': 300.0,
            'description': 'New transaction 2',
            'paid': False,
            'transaction_date': self.DATE_TEST,
            'category': self.category,
            'account': self.account
        }
        Transaction.objects.create(**payloadTransaction)

        transactions = Transaction.objects.all()
        serialized_transactions = TransactionSerializer(
            transactions, many=True)
        res = self.client.get(TRANSACTIONS_URL)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_transactions.data)

    def test_create_valid_transaction_success(self):
        # Test creating transaction with valid payload is successful
        payloadTransaction = {
            'amount': 300.0,
            'description': 'New transaction 2',
            'paid': False,
            'transaction_date': self.DATE_TEST,
            'category': self.category.id,
            'account': self.account.id
        }
        res = self.client.post(TRANSACTIONS_URL, payloadTransaction)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_not_create_transaction_with_empty_data(self):
        # Test not creating a transaction when the data is empty
        payloadTransaction = {
            'amount': '',
            'description': '',
            'paid': False,
            'transaction_date': self.DATE_TEST,
            'category': self.category.id,
            'account': self.account.id
        }

        res = self.client.post(TRANSACTIONS_URL, payloadTransaction)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_transaction_with_wrong_category_id(self):
        # Test not creating a transaction with a wrong category
        WRONG_CATEGORY_ID = 6
        payloadTransaction = {
            'amount': 300.0,
            'description': 'New transaction 2',
            'paid': False,
            'transaction_date': self.DATE_TEST,
            'category': WRONG_CATEGORY_ID,
            'account': self.account.id
        }
        res = self.client.post(TRANSACTIONS_URL, payloadTransaction)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_transaction_with_wrong_account_id(self):
        # Test not creating a transaction with a wrong account
        WRONG_ACCOUNT_ID = 8
        payloadTransaction = {
            'amount': 300.0,
            'description': 'New transaction 2',
            'paid': False,
            'transaction_date': self.DATE_TEST,
            'category': self.category.id,
            'account': WRONG_ACCOUNT_ID
        }
        res = self.client.post(TRANSACTIONS_URL, payloadTransaction)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_transaction_success(self):
        # Test for updating transaction is successful
        payload_partial_updated = {
            'amount': 350.0,
            'description': 'Some other description',
            'paid': False,
        }

        res = self.client.patch(get_detail_transactions_url(
            self.transaction), payload_partial_updated)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount,
                         payload_partial_updated['amount'])
        self.assertEqual(self.transaction.description,
                         payload_partial_updated['description'])

    def test_retrieve_transactions_list_filtered_by_transaction_date(self):
        # Test for filtering transactions
        current_date_transaction_payload = {
            **self.payloadTransaction,
            'transaction_date': self.DATE_TODAY
        }
        Transaction.objects.create(**current_date_transaction_payload)
        for dpm in self.DATES_THIS_MONTH:
            tm_transaction_payload = {
                **self.payloadTransaction,
                'transaction_date': dpm
            }
            Transaction.objects.create(**tm_transaction_payload)
        for dpm in self.DATES_PREVIOUS_MONTH:
            pm_transaction_payload = {
                **self.payloadTransaction,
                'transaction_date': dpm
            }
            Transaction.objects.create(**pm_transaction_payload)

        res = self.client.get(
            get_transactions_url_with_query_args(date_range='today'))
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            get_transactions_url_with_query_args(date_gte='2020-07-01', date_lte='2020-07-31'))
        self.assertEqual(len(res.data), len(self.DATES_PREVIOUS_MONTH))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_transactions_list_filtered_by_account(self):
        # Test for filtering transactions by account
        another_payload_account = {
            **self.payloadAccount,
            'name': 'Another Transactions Account',
        }
        another_account = Account.objects.create(
            **another_payload_account
        )
        transaction_oa_payload = {
            **self.payloadTransaction,
            'account': another_account
        }
        for i in range(3):
            Transaction.objects.create(**transaction_oa_payload)

        res = self.client.get(
            get_transactions_url_with_query_args(account=self.account.id))
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            get_transactions_url_with_query_args(account=another_account.id))
        self.assertEqual(len(res.data), 3)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_transactions_list_filtered_by_category(self):
        # Test for filtering transactions by category
        another_payload_category = {
            **self.payloadCategory,
            'name': 'Another Category',
        }
        another_category = TransactionCategory.objects.create(
            **another_payload_category
        )
        transaction_oc_payload = {
            **self.payloadTransaction,
            'category': another_category
        }
        for i in range(4):
            Transaction.objects.create(**transaction_oc_payload)

        res = self.client.get(
            get_transactions_url_with_query_args(category=self.category.id))
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            get_transactions_url_with_query_args(category=another_category.id))
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_transactions_list_filtered_by_paid(self):
        # Test for filtering transactions by payment state
        paid = True
        for i in range(6):
            paid = not paid
            transaction_cp_payload = {
                **self.payloadTransaction,
                'paid': paid
            }
            Transaction.objects.create(**transaction_cp_payload)

        res = self.client.get(
            get_transactions_url_with_query_args(paid=True))
        self.assertEqual(len(res.data), 3)
        res = self.client.get(
            get_transactions_url_with_query_args(paid=False))
        self.assertEqual(len(res.data), 4)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
