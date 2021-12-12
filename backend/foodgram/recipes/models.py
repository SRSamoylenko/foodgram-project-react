from collections import defaultdict, namedtuple
from typing import List, Tuple

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserFavorites(models.Model):
    user = models.OneToOneField(
        User,
        related_name='favorites',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        primary_key=True,
    )
    recipes = models.ManyToManyField('Recipe', through='FavoriteRecipe')

    class Meta:
        verbose_name = _('User favorite recipe')
        verbose_name_plural = _('User favorite recipes')
        ordering = ('user',)

    def __str__(self):
        return _('{} favorite recipes').format(self.user)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        UserFavorites,
        related_name='+',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='+',
        verbose_name=_('Recipe'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('User favorite recipe')
        verbose_name_plural = _('User favorite recipes')
        constraints = (
            models.UniqueConstraint(
                name='unique_favorite',
                fields=('user', 'recipe'),
            ),
        )
        ordering = ('id',)

    def __str__(self):
        return (
            _('{} likes {}').format(self.user.user, self.recipe)
        )


class UserShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=_('User'),
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    recipes = models.ManyToManyField('Recipe', through='ShoppingCartRecipe')

    class Meta:
        verbose_name = _('User shopping cart')
        ordering = ('user',)

    def __str__(self):
        return _('{} shopping cart').format(self.user)

    def get_ingredients_to_buy(self) -> List[Tuple[str, int, str]]:
        """
        Return list of ingredients with their amount from shopping cart.
        """
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__in=self.recipes.all())
            .select_related('ingredient').all()
        )
        IngredientTuple = namedtuple(
            'IngredientTuple', 'name measurement_unit',
        )
        counter = defaultdict(int)

        for ingredient in ingredients:
            counter[
                IngredientTuple(
                    ingredient.ingredient.name,
                    ingredient.ingredient.measurement_unit
                )
            ] += ingredient.amount
        return [(ingredient.name, amount, ingredient.measurement_unit)
                for ingredient, amount in counter.items()]


class ShoppingCartRecipe(models.Model):
    shopping_cart = models.ForeignKey(
        UserShoppingCart,
        related_name='+',
        verbose_name=_('Shopping cart'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='+',
        verbose_name=_('Recipe'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Shopping cart recipe')
        verbose_name_plural = _('Shopping cart recipes')
        constraints = (
            models.UniqueConstraint(
                name='unique_recipe_for_shopping_cart',
                fields=('shopping_cart', 'recipe'),
            ),
        )
        ordering = ('id',)

    def __str__(self):
        return (
            _('{} added to {}').format(self.recipe, self.shopping_cart)
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
        help_text=_('Enter recipe author'),
        db_index=True,
    )
    name = models.CharField(
        verbose_name=_('Recipe name'),
        max_length=150,
        help_text=_('Enter recipe name'),
        unique=True,
    )
    image = models.ImageField(
        verbose_name=_('Image'),
        upload_to='recipes/images/',
        help_text=_('Enter recipe image'),
    )
    text = models.TextField(
        verbose_name=_('Text'),
        help_text=_('Give recipe description'),
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name=_('Tags'),
        db_index=True,
        help_text=_('Add recipe tags'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Cooking time, min'),
        help_text=_('Add cooking time in minutes'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name=_('Ingredient name'),
        max_length=150,
        help_text=_('Enter ingredient name'),
    )
    measurement_unit = models.CharField(
        verbose_name=_('Measurement unit'),
        max_length=25,
        help_text=_('Enter measurement unit'),
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                name='unique_ingredient_unit',
                fields=('name', 'measurement_unit'),
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('Recipe'),
        related_name='ingredients',
        on_delete=models.CASCADE,
        help_text=_('Enter recipe'),
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('Ingredient'),
        on_delete=models.CASCADE,
        help_text=_('Enter ingredient'),
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('Amount'),
        help_text=_('Enter amount'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Recipe ingredient')
        verbose_name_plural = _('Recipe ingredients')
        ordering = ('recipe', 'ingredient')
        constraints = (
            models.UniqueConstraint(
                name='unique_ingredients',
                fields=('recipe', 'ingredient'),
            ),
        )

    def __str__(self):
        return (
            f'{self.ingredient.name}, '
            f'{self.amount} {self.ingredient.measurement_unit}'
        )


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Tag name'),
        max_length=150,
        unique=True,
        help_text=_('Add tag name'),
    )
    color = ColorField(
        verbose_name=_('Tag color'),
        unique=True,
        help_text=_('Add tag color'),
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
        help_text=_('Add slug'),
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('name', 'slug')

    def __str__(self):
        return f'{self.name}'
