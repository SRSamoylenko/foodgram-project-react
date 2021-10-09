from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name=_('Follower'),
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
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name=_('Ingredients'),
        help_text=_('Enter recipe ingredients'),
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name=_('Tags'),
        db_index=True,
        help_text=_('Add recipe tags'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Cooking time'),
        help_text=_('Add cooking time in minutes'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name=_('Ingredient name'),
        max_length=150,
        help_text=_('Enter ingredient name'),
        unique=True,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Measurement unit'),
        max_length=25,
        help_text=_('Enter measurement unit'),
    )

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('Recipe'),
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
        ordering = ('-created',)
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
    colour = ColorField(
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
