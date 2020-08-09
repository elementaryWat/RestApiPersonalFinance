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
