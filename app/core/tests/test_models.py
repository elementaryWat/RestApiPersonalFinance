from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from core.models import CATEGORY_TYPES


def get_sample_user(email="sample_user@email.com", password="sample_password"):
    # Create a sample user
    return get_user_model().objects.create_user(email, password)


def create_sample_account_type(payload={'name': 'account_testing', 'icon_name': 'testing'}):
    return models.AccountType.objects.create(
        **payload
    )


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        # Test creating a new user with an email is successful
        email = "username@domain.com"
        password = "Test1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

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
        payload = {
            'name': 'account_testing',
            'icon_name': 'testing icon'
        }
        account_type = create_sample_account_type(payload)
        self.assertEqual(str(account_type), payload['name'])
        self.assertEqual(account_type.name, payload['name'])
        self.assertEqual(account_type.icon_name, payload['icon_name'])

    def test_create_account(self):
        # Test creating a new account type
        account_type = create_sample_account_type()
        user = get_sample_user()
        payload = {
            'name': 'Transactions Account',
            'description': 'Some description',
            'account_type': account_type,
            'user': user
        }
        account = models.Account.objects.create(
            **payload
        )
        self.assertEqual(account.name, payload['name'])
        self.assertEqual(account.description, payload['description'])
        self.assertEqual(account.account_type, payload['account_type'])
        self.assertEqual(account.user, payload['user'])

    def test_create_category(self):
        # Test creating a new transaction Category
        user = get_sample_user()
        payload = {
            'name': 'Salary',
            'icon_name': 'salary icon',
            'category_type': CATEGORY_TYPES.INCOME.value,
            'user': user
        }
        category = models.TransactionCategory.objects.create(
            **payload
        )
        self.assertEqual(category.name, payload['name'])
        self.assertEqual(category.icon_name, payload['icon_name'])
        self.assertEqual(category.category_type, payload['category_type'])
        self.assertEqual(category.user, payload['user'])
