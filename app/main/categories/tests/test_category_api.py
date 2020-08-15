from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import TransactionCategory
from django.contrib.auth import get_user_model
from main.categories.serializers import TransactionCategorySerializer

CATEGORIES_URL = reverse('categories:transaction_category-list')


def get_detail_category_url(category):
    return reverse('categories:transaction_category-detail', args=(category.id,))


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
        self.payloadAnotherUser = {
            'email': 'username@domain.com', 'password': 'Test1234'}
        self.anotherUser = get_user_model().objects.create_user(
            **self.payloadAnotherUser
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
        TransactionCategory.objects.create(name="Investments", icon_name="salary",
                                           category_type='IN', user=self.anotherUser)
        category2 = TransactionCategory.objects.create(name="Salary", icon_name="salary",
                                                       category_type='IN', user=self.user)

        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], category2.name)

    def test_create_valid_category_success(self):
        # Test creating category with valid payload is successful
        payload = {
            'name': "Investments",
            'icon_name': "salary",
            'category_type': "IN",
        }

        res = self.client.post(CATEGORIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user'], self.user.id)

    def test_update_category_success(self):
        # Test for updating created categories is successful
        category_to_update = TransactionCategory.objects.create(name="Investments", icon_name="salary",
                                                                category_type='IN', user=self.user)
        payload_updated = {
            'name': "My investments",
            'icon_name': "invest",
            'category_type': "IN",
        }

        res = self.client.put(get_detail_category_url(
            category_to_update), payload_updated)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category_to_update.refresh_from_db()
        self.assertEqual(category_to_update.name, payload_updated['name'])
        self.assertEqual(category_to_update.icon_name,
                         payload_updated['icon_name'])

    def test_not_found_update_category_not_belonging_user(self):
        # Test for not update categories that not belongs the logged user
        category_to_update = TransactionCategory.objects.create(name="Investments", icon_name="salary",
                                                                category_type='IN', user=self.anotherUser)
        payload_updated = {
            'name': "My investments",
            'icon_name': "invest",
            'category_type': "IN",
        }

        res = self.client.put(get_detail_category_url(
            category_to_update), payload_updated)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

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
