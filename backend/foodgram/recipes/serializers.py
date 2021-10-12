from rest_framework import serializers
from djoser.conf import settings

from .models import Tag, Ingredient, Recipe, RecipeIngredient
from .utils import get_decoded_image


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


class CustomImageField(serializers.ImageField):
    def to_internal_value(self, data):
        try:
            image = get_decoded_image(data)
        except UnicodeDecodeError:
            raise serializers.ValidationError('Wrong image format.')
        return image


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
    image = CustomImageField()

    class Meta:
        model = Recipe
        exclude = ('created',)

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False
