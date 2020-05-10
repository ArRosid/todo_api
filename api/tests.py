from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Todo
from api.serializers import TodoSerializer

TODOS_URL = reverse('todo-list')
LOGIN_URL = reverse('login')


class TodoTestCase(TestCase):
    """
        Test Case for todos endpoint
    """

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Test123"
        )

        Todo.objects.create(title="Test default todos")

    def test_login_fail(self):
        """
            Test login wrong credentials
        """
        payload = {
            "username": "wronguser",
            "password": "123",
        }

        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        """
            Test the login ednpoints
        """
        payload = {
            "username": "testuser",
            "password": "Test123",
        }

        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def get_token(self):
        """
            get token
        """
        payload = {
            "username": "testuser",
            "password": "Test123",
        }

        res = self.client.post(LOGIN_URL, payload)
        return res.data["access"]

    def test_get_todos_failed(self):
        """
            Test get todos failed authorization
        """
        res = self.client.get(TODOS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_todos_success(self):
        """
            Test get todos success
        """
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        res = self.client.get(TODOS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_todos(self):
        """
            Test create todos
        """
        payload = {
            "title": "Test todo"
        }

        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        res = self.client.post(TODOS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
