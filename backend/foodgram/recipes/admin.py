from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCartRecipe, Tag, UserFavorites, UserShoppingCart)

EMPTY_VALUE_MESSAGE = _('-empty-')


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class FavoriteRecipeInLine(admin.TabularInline):
    model = FavoriteRecipe
    extra = 1


class ShoppingCartInLine(admin.TabularInline):
    model = ShoppingCartRecipe
    extra = 1


@admin.register(UserFavorites)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = (
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


@admin.register(UserShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'get_recipes',
    )
    inlines = (
        ShoppingCartInLine,
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
        'get_added_to_favorites',
    )
    filter_horizontal = (
        'tags',
    )
    list_filter = (
        'author',
        'tags',
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

    def get_added_to_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()

    get_added_to_favorites.short_description = _('Added to favorites')


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
