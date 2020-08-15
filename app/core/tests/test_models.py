from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from core.models import CATEGORY_TYPES


class ModelTests(TestCase):
    def setUp(self):
        self.payloadUser = {
            'email': 'username@domain.com', 'password': 'Test1234'}
        self.user = get_user_model().objects.create_user(
            **self.payloadUser
        )

        self.payloadAccountType = {
            'name': 'account_testing', 'icon_name': 'testing'}
        self.accountType = models.AccountType.objects.create(
            **self.payloadAccountType
        )

        self.payloadAccount = {
            'name': 'Transactions Account',
            'description': 'Some description',
            'account_type': self.accountType,
            'user': self.user
        }
        self.account = models.Account.objects.create(
            **self.payloadAccount
        )

        self.payloadCategory = {
            'name': 'Salary',
            'icon_name': 'salary icon',
            'category_type': CATEGORY_TYPES.INCOME.value,
            'user': self.user
        }
        self.category = models.TransactionCategory.objects.create(
            **self.payloadCategory
        )

        self.payloadTransaction = {
            'amount': 200.0,
            'description': 'New transaction',
            'paid': True,
            'category': self.category,
            'account': self.account
        }
        self.transaction = models.Transaction.objects.create(
            **self.payloadTransaction
        )

    def test_create_user_with_email_successful(self):
        # Test creating a new user with an email is successful
        self.assertEqual(self.user.email, self.payloadUser['email'])
        self.assertTrue(self.user.check_password(self.payloadUser['password']))

    def test_new_user_email_normalized(self):
        # Test the email for a new user is normalised
        email = 'test@DOMAININUPPERCASE'
        user = get_user_model().objects.create_user(email, 'test1234')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # Test creating user with no email raises error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        # Test creating a new superuser
        user = get_user_model().objects.create_superuser(
            email='test@somedomain.com',
            password='test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_account_type(self):
        # Test creating a new account type
        self.assertEqual(str(self.accountType),
                         self.payloadAccountType['name'])
        self.assertEqual(self.accountType.name,
                         self.payloadAccountType['name'])
        self.assertEqual(self.accountType.icon_name,
                         self.payloadAccountType['icon_name'])

    def test_create_account(self):
        # Test creating a new account
        self.assertEqual(self.account.name, self.payloadAccount['name'])
        self.assertEqual(self.account.description,
                         self.payloadAccount['description'])
        self.assertEqual(self.account.account_type,
                         self.payloadAccount['account_type'])
        self.assertEqual(self.account.user, self.payloadAccount['user'])

    def test_create_category(self):
        # Test creating a new transaction Category
        self.assertEqual(self.category.name, self.payloadCategory['name'])
        self.assertEqual(self.category.icon_name,
                         self.payloadCategory['icon_name'])
        self.assertEqual(self.category.category_type,
                         self.payloadCategory['category_type'])
        self.assertEqual(self.category.user, self.payloadCategory['user'])

    def test_create_transaction(self):
        # Test creating a new transaction
        self.assertEqual(self.transaction.amount,
                         self.payloadTransaction['amount'])
        self.assertEqual(self.transaction.description,
                         self.payloadTransaction['description'])
        self.assertEqual(self.transaction.paid,
                         self.payloadTransaction['paid'])
        self.assertEqual(self.transaction.category,
                         self.payloadTransaction['category'])
        self.assertEqual(self.transaction.account,
                         self.payloadTransaction['account'])
