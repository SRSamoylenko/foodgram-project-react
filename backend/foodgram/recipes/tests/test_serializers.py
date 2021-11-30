from django.test import TestCase

from ..serializers import (IngredientSerializer, RecipeSerializer,
                           RecipeShortSerializer, TagExplicitSerializer)
from . import constants as _


class TestTagSerializer(TestCase):
    def test_fields(self):
        actual_fields = TagExplicitSerializer().get_fields()
        fields = _.TAG_FIELDS

        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in actual_fields)


class TestIngredientSerializer(TestCase):
    def test_fields(self):
        actual_fields = IngredientSerializer().get_fields()
        fields = _.INGREDIENT_FIELDS

        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in actual_fields)


class TestRecipeSerializer(TestCase):
    def test_fields(self):
        actual_fields = RecipeSerializer().get_fields()
        fields = _.RECIPE_SERIALIZER_FIELDS

        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in actual_fields)


class TestRecipeShoppingCartSerializer(TestCase):
    def test_fields(self):
        actual_fields = RecipeShortSerializer().get_fields()
        fields = _.RECIPE_SHOPPING_CART_SERIALIZER_FIELDS

        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in actual_fields)
