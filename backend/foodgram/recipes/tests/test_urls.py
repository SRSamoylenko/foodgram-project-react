from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from ..models import Ingredient, Tag, Recipe
from . import constants as _

User = get_user_model()


class TestTagURLs(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(**_.TEST_TAG)
        self.user = User.objects.create(**_.TEST_USER)

        self.unauthorized_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_urls_names(self):
        tag_urls = {
            _.TAG_LIST_URL: '/api/tags/',
            _.TAG_DETAIL_URL: '/api/tags/1/',
        }
        for actual, expected in tag_urls.items():
            with self.subTest(url=expected):
                self.assertEqual(actual, expected)

    def authorized_user_access(self):
        response = {
            _.TAG_LIST_URL: 200,
            _.TAG_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def unauthorized_user_access(self):
        response = {
            _.TAG_LIST_URL: 200,
            _.TAG_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.unauthorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)


class TestIngredientURLs(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(**_.TEST_INGREDIENT)
        self.user = User.objects.create(**_.TEST_USER)

        self.unauthorized_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_urls_names(self):
        ingredient_urls = {
            _.INGREDIENT_LIST_URL: '/api/ingredients/',
            _.INGREDIENT_DETAIL_URL: '/api/ingredients/1/',
        }
        for actual, expected in ingredient_urls.items():
            with self.subTest(url=expected):
                self.assertEqual(actual, expected)

    def authorized_user_access(self):
        response = {
            _.INGREDIENT_LIST_URL: 200,
            _.INGREDIENT_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def unauthorized_user_access(self):
        response = {
            _.INGREDIENT_LIST_URL: 200,
            _.INGREDIENT_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.unauthorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)


class TestRecipesURLs(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(**_.TEST_INGREDIENT)
        self.tag = Tag.objects.create(**_.TEST_TAG)
        self.author = User.objects.create(**_.TEST_USER)
        self.recipe = Recipe.objects.create(
            author=self.author, **_.TEST_RECIPE
        )
        self.user = User.objects.create(**_.TEST_USER_2)

        self.unauthorized_client = APIClient()
        self.author_client = APIClient()
        self.author_client.force_authenticate(self.author)
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_url_names(self):
        recipe_urls = {
            _.RECIPE_LIST_URL: '/api/recipes/',
            _.RECIPE_DETAIL_URL: '/api/recipes/1/',
        }
        for actual, expected in recipe_urls.items():
            with self.subTest(url=expected):
                self.assertEqual(actual, expected)

    def unauthorized_user_list_detail_access(self):
        response = {
            _.RECIPE_LIST_URL: 200,
            _.RECIPE_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.unauthorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def unauthorized_user_create_access(self):
        response = self.unauthorized_client.post(_.RECIPE_LIST_URL, data=_.TEST_RECIPE_2)
        self.assertEqual(response.status_code, 401)

    def unauthorized_user_update_access(self):
        response = self.unauthorized_client.put(_.RECIPE_DETAIL_URL, data=_.TEST_RECIPE_2)
        self.assertEqual(response.status_code, 401)

    def unauthorized_user_delete_access(self):
        response = self.unauthorized_client.delete(_.RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, 401)

    def authorized_user_list_detail_access(self):
        response = {
            _.RECIPE_LIST_URL: 200,
            _.RECIPE_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def authorized_user_create_access(self):
        response = self.authorized_client.post(_.RECIPE_LIST_URL, data=_.TEST_RECIPE_2)
        self.assertEqual(response.status_code, 200)

    def authorized_user_update_access(self):
        response = self.authorized_client.put(_.RECIPE_DETAIL_URL, data=_.TEST_RECIPE_2)
        self.assertEqual(response.status_code, 403)

    def authorized_user_delete_access(self):
        response = self.authorized_client.delete(_.RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, 403)

    def author_user_list_detail_access(self):
        response = {
            _.RECIPE_LIST_URL: 200,
            _.RECIPE_DETAIL_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def author_user_create_access(self):
        response = self.author_client.post(_.RECIPE_LIST_URL, data=_.TEST_RECIPE_2)
        self.assertEqual(response.status_code, 200)

    def author_user_update_access(self):
        response = self.author_client.put(_.RECIPE_DETAIL_URL, data=_.TEST_RECIPE_2)
        self.assertEqual(response.status_code, 200)

    def author_user_delete_access(self):
        response = self.author_client.delete(_.RECIPE_DETAIL_URL)
        self.assertEqual(response.status_code, 204)


class TestShoppingCartURLs(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create(**_.TEST_USER)
        self.recipe = Recipe.objects.create(
            author=self.author, **_.TEST_RECIPE
        )
        self.user = User.objects.create(**_.TEST_USER_2)

        self.unauthorized_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_url_names(self):
        urls = {
            _.SHOPPING_CART_URL: '/api/recipes/1/shopping_cart/',
            _.DOWNLOAD_SHOPPING_CART_URL: '/api/recipes/download_shopping_cart/'
        }
        for actual, expected in urls.items():
            with self.subTest(url=expected):
                self.assertEqual(actual, expected)

    def test_unauthorized_user_get_access(self):
        response = {
            _.SHOPPING_CART_URL: 401,
            _.DOWNLOAD_SHOPPING_CART_URL: 401,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.unauthorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def test_unauthorized_user_delete_access(self):
        response = self.unauthorized_client.delete(_.SHOPPING_CART_URL)
        self.assertEqual(response.status_code, 401)

    def test_authorized_user_get_access(self):
        response = {
            _.SHOPPING_CART_URL: 201,
            _.DOWNLOAD_SHOPPING_CART_URL: 200,
        }
        for url, expected_response in response.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.authorized_client.get(url)
                self.assertEqual(expected_response, response.status_code)

    def test_authorized_user_delete_access(self):
        response = self.authorized_client.get(_.SHOPPING_CART_URL)
        self.assertEqual(response.status_code, 201)

        response = self.authorized_client.delete(_.SHOPPING_CART_URL)
        self.assertEqual(response.status_code, 204)

    def test_add_recipe_twice(self):
        response = self.authorized_client.get(_.SHOPPING_CART_URL)
        self.assertEqual(response.status_code, 201)

        response = self.authorized_client.get(_.SHOPPING_CART_URL)
        self.assertEqual(response.status_code, 400)

    def delete_not_existed_recipe(self):
        response = self.authorized_client.delete(_.SHOPPING_CART_URL)
        self.assertEqual(response.status_code, 400)


class TestFavoritesURLs(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create(**_.TEST_USER)
        self.recipe = Recipe.objects.create(
            author=self.author, **_.TEST_RECIPE
        )
        self.user = User.objects.create(**_.TEST_USER_2)

        self.unauthorized_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_url_names(self):
        self.assertEqual(_.FAVORITE_URL, '/api/recipes/1/favorite/')

    def test_unauthorized_user_access(self):
        response = self.unauthorized_client.get(_.FAVORITE_URL)
        self.assertEqual(response.status_code, 401)

        response = self.unauthorized_client.delete(_.FAVORITE_URL)
        self.assertEqual(response.status_code, 401)

    def test_authorized_user_access(self):
        response = self.authorized_client.get(_.FAVORITE_URL)
        self.assertEqual(response.status_code, 201)

        response = self.authorized_client.get(_.FAVORITE_URL)
        self.assertEqual(response.status_code, 400)

        response = self.authorized_client.delete(_.FAVORITE_URL)
        self.assertEqual(response.status_code, 204)

        response = self.authorized_client.delete(_.FAVORITE_URL)
        self.assertEqual(response.status_code, 400)
