from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**args):
    return get_user_model().objects.create_user(**args)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # Test creating user with valid payload is successful
        payload = {
            'email': "testuser@normal.com",
            'password': "normal234",
            'name': "Normal User"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_existing_user(self):
        # Test creating an user that already exists fails
        payload = {
            'email': "testuser@normal.com",
            'password': "anypassword",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password(self):
        # Test creating an user with a short password fails
        payload = {
            'email': "testuser@normal.com",
            'password': "sho",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        # Test creating a token for an existing user
        payload = {
            'email': "testuser@domain.com",
            'password': "validpassword",
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        # Test that token is not created for invalid credentials
        create_user(email="testuser@normal.com", password="validpassword")
        payload = {
            'email': "testuser@domain.com",
            'password': "invalidpassword",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        # Test that token is not created when the user doesn't exist
        payload = {
            'email': "nonexistinguser@domain.com",
            'password': "nonexisting",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_fields(self):
        # Test that token is not created when some fields are not given
        payload = {
            'email': "nonexistinguser@domain.com",
            'password': "",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrive_profile_not_authenticated(self):
        # Test authentication is required for retrieve user profile
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    # Test API requests that require authentication
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="testemail@test.com",
            password="test1234"
        )
        self.client.force_authenticate(self.user)

    def test_retrive_profile_success(self):
        # Test retrieving user profile for logged in user
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        # Test retrieving user profile for logged in user
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        # Test updating user data
        payload = {
            'name': "new name",
            'password': "new password",
        }
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
