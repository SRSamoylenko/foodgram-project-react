from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import permissions

from .models import (
    Tag,
    Ingredient,
    Recipe,
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListRetrieveSerializer,
    RecipeCreateUpdateSerializer,
)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeListRetrieveSerializer
        return RecipeCreateUpdateSerializer
