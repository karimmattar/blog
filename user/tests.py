"""
User tests cases
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class UserTestCase(TestCase):
    """
    User test cases
    """

    def setUp(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            email="exist@test.com",
            username="exist",
            password="T@eST1926",
        )
        self.client = APIClient()

    def test_user_create_success(self):
        """
        test create user in success
        :return:
        """
        body = {
            "email": "test@test.com",
            "password": "T@eST1926",
        }
        response = self.client.post("/api/auth/create/", body)
        self.assertEqual(response.status_code, 201)

    def test_user_create_invalid_password(self):
        """
        test user create with invalid password criteria
        :return:
        """
        body = {
            "email": "test@test.com",
            "password": "test",
        }
        response = self.client.post("/api/auth/create/", body)
        self.assertEqual(response.status_code, 400)

    def test_user_create_missing_data(self):
        """
        test user create with missing data
        :return:
        """
        body = {
            "email": "test@test.com",
        }
        response = self.client.post("/api/auth/create/", body)
        self.assertEqual(response.status_code, 400)

    def test_user_create_email_exists(self):
        """
        test user create with exist email
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        response = self.client.post("/api/auth/create/", body)
        self.assertEqual(response.status_code, 400)

    def test_token(self):
        """
        test token
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        response = self.client.post("/api/auth/token/", body)
        self.assertEqual(response.status_code, 200)

    def test_token_refresh(self):
        """
        test token resfresh
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        tokens = self.client.post("/api/auth/token/", body)
        response = self.client.post(
            "/api/auth/token/refresh/", {"refresh": tokens.data["refresh"]}
        )
        self.assertEqual(response.status_code, 200)

    def test_token_verify(self):
        """
        test token verify
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        tokens = self.client.post("/api/auth/token/", body)
        response = self.client.post(
            "/api/auth/token/verify/", {"token": tokens.data["access"]}
        )
        self.assertEqual(response.status_code, 200)

    def test_token_blacklist(self):
        """
        test token blacklist
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        tokens = self.client.post("/api/auth/token/", body)
        response = self.client.post(
            "/api/auth/token/blacklist/", {"refresh": tokens.data["refresh"]}
        )
        self.assertEqual(response.status_code, 200)

    def test_user_retrieve(self):
        """
        test retrieve user
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        tokens = self.client.post("/api/auth/token/", body)
        response = self.client.get(
            "/api/auth/me/",
            headers={"Authorization": f"Bearer {tokens.data['access']}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_user_update(self):
        """
        test update user
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        tokens = self.client.post("/api/auth/token/", body)
        _data = {
            "first_name": "test",
            "last_name": "test",
        }
        response = self.client.patch(
            "/api/auth/me/",
            _data,
            headers={"Authorization": f"Bearer {tokens.data['access']}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_user_password_change(self):
        """
        test update user
        :return:
        """
        body = {
            "email": "exist@test.com",
            "password": "T@eST1926",
        }
        tokens = self.client.post("/api/auth/token/", body)
        _data = {
            "old_password": "T@eST1926",
            "new_password": "ST@eST1926",
        }
        response = self.client.put(
            "/api/auth/me/password/",
            _data,
            headers={"Authorization": f"Bearer {tokens.data['access']}"},
        )
        self.assertEqual(response.status_code, 200)
