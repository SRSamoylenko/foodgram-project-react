from rest_framework import serializers
from djoser.conf import settings
from rest_framework.generics import get_object_or_404
from drf_extra_fields.fields import Base64ImageField

from .models import Tag, Ingredient, Recipe, RecipeIngredient


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

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
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
