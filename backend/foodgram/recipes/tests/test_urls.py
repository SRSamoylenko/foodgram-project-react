from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Ingredient, Tag
from . import constants as _

User = get_user_model()


class TestTagURLs(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(**_.TEST_TAG)
        self.user = User.objects.create(**_.TEST_USER)

        self.unauthorized_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_names(self):
        tag_urls = {
            _.TAG_LIST_URL: '/api/tags/',
            _.TAG_DETAIL_URL: '/api/tags/1/',
        }
        for actual, expected in tag_urls.items():
            with self.subTest(url=expected):
                self.assertEqual(actual, expected)

    def authorized_user_access(self):
        authorized_response = {
            _.TAG_LIST_URL: 200,
            _.TAG_DETAIL_URL: 200,
        }
        for url, expected_response in authorized_response.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def unauthorized_user_access(self):
        unauthorized_response = {
            _.TAG_LIST_URL: 200,
            _.TAG_DETAIL_URL: 200,
        }
        for url, expected_response in unauthorized_response.items():
            with self.subTest(url=url):
                response = self.unauthorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)


class TestIngredientURLs(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(**_.TEST_INGREDIENT)
        self.user = User.objects.create(**_.TEST_USER)

        self.unauthorized_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_names(self):
        ingredient_urls = {
            _.INGREDIENT_LIST_URL: '/api/ingredients/',
            _.INGREDIENT_DETAIL_URL: '/api/ingredients/1/',
        }
        for actual, expected in ingredient_urls.items():
            with self.subTest(url=expected):
                self.assertEqual(actual, expected)

    def authorized_user_access(self):
        authorized_response = {
            _.INGREDIENT_LIST_URL: 200,
            _.INGREDIENT_DETAIL_URL: 200,
        }
        for url, expected_response in authorized_response.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def unauthorized_user_access(self):
        unauthorized_response = {
            _.INGREDIENT_LIST_URL: 200,
            _.INGREDIENT_DETAIL_URL: 200,
        }
        for url, expected_response in unauthorized_response.items():
            with self.subTest(url=url):
                response = self.unauthorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)
