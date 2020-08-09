from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import TransactionCategory
from main.categories.serializers import TransactionCategorySerializer

CATEGORIES_URL = reverse('categories:transaction_category-list')


class PublicAccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrive_profile_not_authenticated(self):
        # Test authentication is required for retrieve user profile
        res = self.client.get(CATEGORIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_category_when_not_logged(self):
        # Test not creating a category when the user is not logged
        payload = {
            'name': "Investments",
            'icon_name': "salary",
            'category_type': "IN",
        }

        res = self.client.post(CATEGORIES_URL, payload)
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

    def test_retrieve_categories_list(self):
        # Test for showing created categories
        TransactionCategory.objects.create(name="Salary", icon_name="salary",
                                           category_type='IN', user=self.user)
        TransactionCategory.objects.create(name="Investments", icon_name="salary",
                                           category_type='IN', user=self.user)

        categories = TransactionCategory.objects.all().order_by('name')
        serialized_categories = TransactionCategorySerializer(
            categories, many=True)
        res = self.client.get(CATEGORIES_URL)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialized_categories.data)

    def test_retrieve_categories_list_limited_to_user(self):
        # Test for showing created categories for the logged in user
        another_user = get_user_model().objects.create_user(
            email="another@test.com",
            password="test1234"
        )

        TransactionCategory.objects.create(name="Investments", icon_name="salary",
                                           category_type='IN', user=another_user)
        category2 = TransactionCategory.objects.create(name="Salary", icon_name="salary",
                                                       category_type='IN', user=self.user)

        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], category2.name)

    def test_create_valid_account_success(self):
        # Test creating category with valid payload is successful
        payload = {
            'name': "Investments",
            'icon_name': "salary",
            'category_type': "IN",
        }

        res = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user'], self.user.id)

    def test_not_create_category_with_empty_data(self):
        # Test not creating a category when the data is empty
        payload = {
            'name': "",
            'icon_name': "",
            'category_type': "",
        }

        res = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_category_with_wrong_category(self):
        # Test not creating a category when the data is empty
        payload = {
            'name': "Investments",
            'icon_name': "salary",
            'category_type': "wrong",
        }

        res = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
