from rest_framework import serializers
from djoser.conf import settings
from drf_extra_fields.fields import Base64ImageField

from .models import Tag, Ingredient, Recipe, RecipeIngredient, UserFavorites


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
        favorites, created = UserFavorites.objects.get_or_create(user=user)
        return recipe in favorites.recipes.all()

    def get_is_in_shopping_cart(self, recipe):
        return False

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
        return RecipeShortSerializer(user.recipes.all(), many=True, context=self.context).data

    @staticmethod
    def get_recipes_count(user):
        return user.recipes.count()
