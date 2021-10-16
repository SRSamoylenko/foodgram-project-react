from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import permissions, status, serializers
from django.utils.translation import gettext_lazy as _

from .models import (
    Tag,
    Ingredient,
    Recipe,
)
from .serializers import (
    TagExplicitSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeShortSerializer,
)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagExplicitSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.action == 'favorite':
            self.permission_classes = [permissions.IsAuthenticated],
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'favorite':
            return RecipeShortSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=('get', 'delete'),
    )
    def favorite(self, request, id=None):
        operation = {
            'GET': self.add_favorite,
            'DELETE': self.remove_favorite,
        }
        return operation[request.method](request, id)

    def add_favorite(self, request, id=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)

        if self.can_add_favorite(user, recipe, raise_exception=True):
            user.favorites.recipes.add(recipe)

        context = {'request': request}
        serializer = self.get_serializer(
            recipe,
            context=context,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def can_add_favorite(user, recipe, raise_exception=True):
        if recipe in user.favorites.recipes:
            if raise_exception:
                raise serializers.ValidationError(_('Cannot add to favorites twice.'))
            return False
        return True

    def remove_favorite(self, request, id=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)

        if self.can_remove_favorite(user, recipe, raise_exception=True):
            user.favorites.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def can_remove_favorite(user, recipe, raise_exception=True):
        if recipe not in user.favorites.recipes:
            if raise_exception:
                raise serializers.ValidationError(_('Not a favorite recipe.'))
            return False
        return True
