from djoser.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers

from .models import (Ingredient, Recipe, RecipeIngredient, Tag, UserFavorites,
                     UserShoppingCart)


class TagExplicitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, instance):
        return TagExplicitSerializer(instance).data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientExplicitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id',
        read_only=True,
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True,
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(
        min_value=1,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

    def to_representation(self, instance):
        return RecipeIngredientExplicitSerializer(instance).data


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, queryset=Tag.objects.all())
    author = settings.SERIALIZERS.user(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('created',)

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        favorites, _ = UserFavorites.objects.prefetch_related(
            'recipes'
        ).get_or_create(user=user)
        return recipe in favorites.recipes.all()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        shopping_cart, _ = UserShoppingCart.objects.prefetch_related(
            'recipes'
        ).get_or_create(user=user)
        return recipe in shopping_cart.recipes.all()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)
        for ingredient_data in ingredients_data:
            recipe.ingredients.create(
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount'],
            )
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for field, value in validated_data.items():
            recipe.__setattr__(field, value)

        recipe.tags.clear()
        recipe.tags.set(tags)

        recipe.ingredients.all().delete()
        for ingredient_data in ingredients_data:
            recipe.ingredients.create(
                ingredient=ingredient_data['id'],
                amount=ingredient_data['amount'],
            )
        recipe.save()
        return recipe

    @staticmethod
    def validate_ingredients(ingredients):
        checked_ingredients = set()
        for ingredient in ingredients:
            if ingredient['id'].id in checked_ingredients:
                raise serializers.ValidationError(
                    'Ingredients have to be unique.'
                )
            checked_ingredients.add(ingredient['id'].id)
        return ingredients

    @staticmethod
    def validate_tags(tags):
        checked_tags = set()
        for tag in tags:
            if tag.id in checked_tags:
                raise serializers.ValidationError('Tags have to be unique.')
            checked_tags.add(tag.id)
        return tags


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(settings.SERIALIZERS.user):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(settings.SERIALIZERS.user.Meta):
        fields = settings.SERIALIZERS.user.Meta.fields + (
            'recipes', 'recipes_count'
        )

    def get_recipes(self, user):
        queryset = user.recipes.all()
        limit = self.context['request'].query_params.get('recipes_limit')
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                raise exceptions.ParseError(
                    'recipes_limit query param must be an integer.'
                )
            else:
                queryset = queryset[:limit]
        return RecipeShortSerializer(
            queryset,
            many=True,
            context=self.context
        ).data

    @staticmethod
    def get_recipes_count(user):
        return user.recipes.count()
