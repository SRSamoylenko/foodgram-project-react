from django.contrib import admin

from .models import (
    Recipe,
    Ingredient,
    RecipeIngredient,
    Tag,
)

from django.utils.translation import gettext_lazy as _

EMPTY_VALUE_MESSAGE = _('-empty-')


class TagInLine(admin.TabularInline):
    model = Tag
    extra = 1


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk'
        'author',
        'name',
        'image',
        'text',
        'get_ingredients',
        'get_tags',
        'cooking_time',
    )
    filter_horizontal = (
        'ingredients',
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
        TagInLine,
        RecipeIngredientInLine,
    )
    empty_value_display = EMPTY_VALUE_MESSAGE

    def get_tags(self, obj):
        tags = obj.tags.values_list('name', flat=True)
        return ', '.join(tags)

    get_tags.short_description = _('Tags')

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        return '\n'.join(ingredients)

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


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
    list_filter = (
        'recipe',
        'ingredient',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'colour',
        'slug',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE
