from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                      ShoppingCartRecipe, Tag, UserFavorites, UserShoppingCart)
from . import constants as _

User = get_user_model()


class RecipeTest(TestCase):
    def test_fields(self):  # noqa
        """Check Recipe fields."""
        for field, expected_values in _.RECIPE_FIELDS.items():
            with self.subTest(field=field):
                for option, expected_value in expected_values.items():
                    with self.subTest(option=option):
                        self.assertEqual(
                            Recipe._meta.get_field(field).__dict__[option],
                            expected_value
                        )

    def test_object_name(self):
        """Check Recipe __str__ output."""
        test_user = User.objects.create(**_.TEST_USER)
        test_recipe = Recipe.objects.create(
            author=test_user,
            **_.TEST_RECIPE,
        )
        expected_output = _.RECIPE_STR_OUTPUT.format(**test_recipe.__dict__)
        self.assertEqual(expected_output, str(test_recipe))


class IngredientTest(TestCase):
    def test_fields(self):  # noqa
        """Check Ingredient fields."""
        for field, expected_values in _.INGREDIENT_FIELDS.items():
            with self.subTest(field=field):
                for option, expected_value in expected_values.items():
                    with self.subTest(option=option):
                        self.assertEqual(
                            Ingredient._meta.get_field(field).__dict__[option],
                            expected_value
                        )

    def test_object_name(self):
        """Check Ingredient __str__ output."""
        test_ingredient = Ingredient.objects.create(**_.TEST_INGREDIENT)
        expected_output = _.INGREDIENT_STR_OUTPUT.format(
            **test_ingredient.__dict__
        )
        self.assertEqual(expected_output, str(test_ingredient))


class RecipeIngredientTest(TestCase):
    def test_fields(self):  # noqa
        """Check RecipeIngredient fields."""
        for field, expected_values in _.RECIPE_INGREDIENT_FIELDS.items():
            with self.subTest(field=field):
                for option, expected_value in expected_values.items():
                    with self.subTest(option=option):
                        self.assertEqual(
                            (RecipeIngredient._meta
                                .get_field(field)
                                .__dict__[option]),
                            expected_value
                        )

    def test_object_name(self):
        """Check RecipeIngredient __str__ output."""
        test_user = User.objects.create(**_.TEST_USER)
        test_recipe = Recipe.objects.create(
            author=test_user,
            **_.TEST_RECIPE,
        )
        test_ingredient = Ingredient.objects.create(**_.TEST_INGREDIENT)
        test_recipe_ingredient = RecipeIngredient.objects.create(
            recipe=test_recipe,
            ingredient=test_ingredient,
            **_.TEST_RECIPE_INGREDIENT,
        )
        expected_output = _.RECIPE_INGREDIENT_STR_OUTPUT.format(
            ingredient_name=test_ingredient.name,
            measurement_unit=test_ingredient.measurement_unit,
            **test_recipe_ingredient.__dict__,
        )
        self.assertEqual(expected_output, str(test_recipe_ingredient))


class TagTest(TestCase):
    def test_fields(self):  # noqa
        """Check Tag fields."""
        for field, expected_values in _.TAG_FIELDS.items():
            with self.subTest(field=field):
                for option, expected_value in expected_values.items():
                    with self.subTest(option=option):
                        self.assertEqual(
                            Tag._meta.get_field(field).__dict__[option],
                            expected_value
                        )

    def test_object_name(self):
        """Check Tag __str__ output."""
        test_tag = Tag.objects.create(**_.TEST_TAG)
        expected_output = _.TAG_STR_OUTPUT.format(**test_tag.__dict__)
        self.assertEqual(expected_output, str(test_tag))


class UserFavoritesTest(TestCase):
    def test_object_name(self):
        """Check UserFavorites __str__ output."""
        test_user = User.objects.create(**_.TEST_USER)
        test_recipe = Recipe.objects.create(author=test_user, **_.TEST_RECIPE)
        test_user_favorites = UserFavorites.objects.create(user=test_user)
        test_user_favorites.recipes.add(test_recipe)
        expected_output = _.USER_FAVORITES_STR_OUTPUT.format(test_user)
        self.assertEqual(expected_output, str(test_user_favorites))


class FavoriteRecipeTest(TestCase):
    def test_object_name(self):
        """Check FavoriteRecipe __str__ output."""
        test_user = User.objects.create(**_.TEST_USER)
        test_recipe = Recipe.objects.create(author=test_user, **_.TEST_RECIPE)
        test_user_favorites = UserFavorites.objects.create(user=test_user)
        test_favorite_recipe = FavoriteRecipe.objects.create(
            user=test_user_favorites,
            recipe=test_recipe,
        )
        expected_output = _.FAVORITE_RECIPE_STR_OUTPUT.format(
            test_user, test_recipe,
        )
        self.assertEqual(expected_output, str(test_favorite_recipe))


class UserShoppingCartTest(TestCase):
    def test_object_name(self):
        """Check UserShoppingCart __str__ output."""
        test_user = User.objects.create(**_.TEST_USER)
        test_recipe = Recipe.objects.create(author=test_user, **_.TEST_RECIPE)
        test_user_shopping_cart = (
            UserShoppingCart.objects.create(user=test_user)
        )
        test_user_shopping_cart.recipes.add(test_recipe)
        expected_output = _.USER_SHOPPING_CART_STR_OUTPUT.format(test_user)
        self.assertEqual(expected_output, str(test_user_shopping_cart))


class ShoppingCartRecipeTest(TestCase):
    def test_object_name(self):
        """Check ShoppingCartRecipe __str__ output."""
        test_user = User.objects.create(**_.TEST_USER)
        test_recipe = Recipe.objects.create(author=test_user, **_.TEST_RECIPE)
        test_user_shopping_cart = UserShoppingCart.objects.create(
            user=test_user
        )
        test_shopping_cart_recipe = ShoppingCartRecipe.objects.create(
            shopping_cart=test_user_shopping_cart,
            recipe=test_recipe,
        )
        expected_output = _.SHOPPING_CART_STR_OUTPUT.format(
            test_recipe, test_user_shopping_cart,
        )
        self.assertEqual(expected_output, str(test_shopping_cart_recipe))
