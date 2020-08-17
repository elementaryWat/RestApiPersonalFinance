from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Transaction, Account, AccountType, TransactionCategory, CATEGORY_TYPES
import datetime
from main.transactions.serializers import TransactionSerializer

TRANSACTIONS_URL = reverse('transactions:transactions-list')


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

        self.DATE_TODAY = datetime.date.today()
        self.payloadTransaction = {
            'amount': 200.0,
            'description': 'New transaction',
            'paid': False,
            'transaction_date': self.DATE_TODAY,
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
        self.assertEqual(transaction_serialized.data['amount'],
                         res.data['amount'])
        self.assertEqual(transaction_serialized.data['description'],
                         res.data['description'])
        self.assertEqual(transaction_serialized.data['paid'],
                         res.data['paid'])
        self.assertEqual(transaction_serialized.data['category'],
                         res.data['category'])
        self.assertEqual(transaction_serialized.data['account'],
                         res.data['account'])

    def test_retrieve_transactions_list(self):
        # Test for showing created transactions
        payloadTransaction = {
            'amount': 300.0,
            'description': 'New transaction 2',
            'paid': False,
            'transaction_date': self.DATE_TODAY,
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
            'transaction_date': self.DATE_TODAY,
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
            'transaction_date': self.DATE_TODAY,
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
            'transaction_date': self.DATE_TODAY,
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
            'transaction_date': self.DATE_TODAY,
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
