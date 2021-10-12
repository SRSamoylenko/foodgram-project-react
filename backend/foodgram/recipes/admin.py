from django.contrib import admin

from .models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    Tag, UserFavorite,
    FavoriteRecipe,
)

from django.utils.translation import gettext_lazy as _

EMPTY_VALUE_MESSAGE = _('-empty-')


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class FavoriteRecipeInLine(admin.TabularInline):
    model = FavoriteRecipe
    extra = 1


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'get_recipes',
    )
    inlines = (
        FavoriteRecipeInLine,
    )
    list_filter = (
        'user',
        'recipes',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return ' | '.join([str(recipe) for recipe in recipes])

    get_recipes.short_description = _('Recipes')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'image',
        'text',
        'get_ingredients',
        'get_tags',
        'cooking_time',
    )
    filter_horizontal = (
        'tags',
    )
    list_filter = (
        'author',
    )
    search_fields = (
        'name',
        'text',
    )
    inlines = (
        RecipeIngredientInLine,
    )
    empty_value_display = EMPTY_VALUE_MESSAGE

    def get_tags(self, obj):
        tags = obj.tags.values_list('name', flat=True)
        return ', '.join(tags)

    get_tags.short_description = _('Tags')

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        return ' | '.join([str(ingredient) for ingredient in ingredients])

    get_ingredients.short_description = _('Ingredients')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE
