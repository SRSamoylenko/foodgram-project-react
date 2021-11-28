from django.urls import reverse
from django.utils.translation import gettext_lazy as _

TEST_USER = {
    'first_name': 'test',
    'last_name': 'test',
    'email': 'test@test.com',
}

TEST_RECIPE = {
    'name': 'test',
    'text': 'test',
    'cooking_time': 5,
}

RECIPE_STR_OUTPUT = '{name}'

TEST_INGREDIENT = {
    'name': 'test',
    'measurement_unit': 'кг',
}

INGREDIENT_STR_OUTPUT = '{name}, {measurement_unit}'

TEST_RECIPE_INGREDIENT = {
    'amount': 5,
}

RECIPE_INGREDIENT_STR_OUTPUT = '{ingredient_name}, {amount} {measurement_unit}'

TEST_TAG = {
    'name': 'test',
    'color': '#138256',
    'slug': 'test',
}

TAG_STR_OUTPUT = '{name}'

USER_FAVORITES_STR_OUTPUT = _('{} favorite recipes')

FAVORITE_RECIPE_STR_OUTPUT = _('{} likes {}')

USER_SHOPPING_CART_STR_OUTPUT = _('{} shopping cart')

SHOPPING_CART_STR_OUTPUT = _('{} added to {}')

RECIPE_FIELDS = {
    'author': {
        'verbose_name': _('Author'),
        'help_text': _('Enter recipe author'),
        'db_index': True,
    },
    'name': {
        'verbose_name': _('Recipe name'),
        'max_length': 150,
        'help_text': _('Enter recipe name'),
    },
    'image': {
        'verbose_name': _('Image'),
        'upload_to': 'recipes/images/',
        'help_text': _('Enter recipe image'),
    },
    'text': {
        'verbose_name': _('Text'),
        'help_text': _('Give recipe description'),
    },
    'tags': {
        'verbose_name': _('Tags'),
        'db_index': True,
        'help_text': _('Add recipe tags'),
    },
    'cooking_time': {
        'verbose_name': _('Cooking time, min'),
        'help_text': _('Add cooking time in minutes'),
    },
    'created': {
        'auto_now_add': True,
        'db_index': True,
    },
}

INGREDIENT_FIELDS = {
    'name': {
        'verbose_name': _('Ingredient name'),
        'max_length': 150,
        'help_text': _('Enter ingredient name'),
    },
    'measurement_unit': {
        'verbose_name': _('Measurement unit'),
        'max_length': 25,
        'help_text': _('Enter measurement unit'),
    },
}

RECIPE_INGREDIENT_FIELDS = {
    'recipe': {
        'verbose_name': _('Recipe'),
        'help_text': _('Enter recipe'),
    },
    'ingredient': {
        'verbose_name': _('Ingredient'),
        'help_text': _('Enter ingredient'),
    },
    'amount': {
        'verbose_name': _('Amount'),
        'help_text': _('Enter amount'),
    },
    'created': {
        'auto_now_add': True,
        'db_index': True,
    },
}

TAG_FIELDS = {
    'name': {
        'verbose_name': _('Tag name'),
        'max_length': 150,
        'help_text': _('Add tag name'),
    },
    'color': {
        'verbose_name': _('Tag color'),
        'help_text': _('Add tag color'),
    },
    'slug': {
        'verbose_name': _('Slug'),
        'help_text': _('Add slug'),
    },
}

TAG_LIST_URL = reverse(
    'recipes:tag-list',
)
TAG_DETAIL_URL = reverse(
    'recipes:tag-detail',
    kwargs={'pk': 1},
)

INGREDIENT_LIST_URL = reverse(
    'recipes:ingredient-list',
)
INGREDIENT_DETAIL_URL = reverse(
    'recipes:ingredient-detail',
    kwargs={'pk': 1},
)
