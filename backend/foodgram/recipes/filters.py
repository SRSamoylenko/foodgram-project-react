from django_filters import rest_framework as filters
from .models import Recipe, Tag, UserFavorites, UserShoppingCart


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter',
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    def is_favorited_filter(self, queryset, name, is_favorited):
        user = self.request.user
        if user.is_anonymous:
            favorite_recipes = {}
        else:
            favorites, created = UserFavorites.objects.prefetch_related('recipes').get_or_create(user=user)
            favorite_recipes = favorites.recipes.all()
        if not is_favorited:
            return queryset.exclude(id__in=favorite_recipes)
        return queryset.filter(id__in=favorite_recipes)

    def is_in_shopping_cart_filter(self, queryset, name, is_in_shopping_cart):
        user = self.request.user
        if user.is_anonymous:
            shopping_cart_recipes = {}
        else:
            shopping_cart, created = UserShoppingCart.objects.prefetch_related('recipes').get_or_create(user=user)
            shopping_cart_recipes = shopping_cart.recipes.all()
        if not is_in_shopping_cart:
            return queryset.exclude(id__in=shopping_cart_recipes)
        return queryset.filter(id__in=shopping_cart_recipes)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
