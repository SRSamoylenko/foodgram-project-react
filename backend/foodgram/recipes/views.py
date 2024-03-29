import io

from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag, UserFavorites, UserShoppingCart
from .permissions import IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeShortSerializer, TagExplicitSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagExplicitSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RecipeFilter
    ordering = ('-created',)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action == 'favorite':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'shopping_cart':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'download_shopping_cart':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'favorite':
            return RecipeShortSerializer
        elif self.action == 'shopping_cart':
            return RecipeShortSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=('get', 'delete'),
    )
    def favorite(self, request, pk=None):
        operation = {
            'GET': self.add_favorite,
            'DELETE': self.remove_favorite,
        }
        return operation[request.method](request, pk)

    def add_favorite(self, request, pk=None):
        user_favorites, created = UserFavorites.objects.prefetch_related(
            'recipes'
        ).get_or_create(user=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.can_add_favorite(user_favorites, recipe, raise_exception=True):
            user_favorites.recipes.add(recipe)

        context = {'request': request}
        serializer = self.get_serializer(
            recipe,
            context=context,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def can_add_favorite(favorites, recipe, raise_exception=True):
        if recipe in favorites.recipes.all():
            if raise_exception:
                raise ValidationError(_('Cannot add to favorites twice.'))
            return False
        return True

    def remove_favorite(self, request, id=None):
        favorites, created = UserFavorites.objects.prefetch_related(
            'recipes'
        ).get_or_create(user=request.user)
        recipe = get_object_or_404(Recipe, id=id)

        if self.can_remove_favorite(favorites, recipe, raise_exception=True):
            favorites.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def can_remove_favorite(favorites, recipe, raise_exception=True):
        if recipe not in favorites.recipes.all():
            if raise_exception:
                raise ValidationError(_('Not a favorite recipe.'))
            return False
        return True

    @action(
        detail=True,
        methods=('get', 'delete'),
        url_name='shopping-cart',
    )
    def shopping_cart(self, request, pk=None):
        operation = {
            'GET': self.add_to_shopping_cart,
            'DELETE': self.remove_from_shopping_cart,
        }
        return operation[request.method](request, pk)

    def add_to_shopping_cart(self, request, pk=None):
        shopping_cart, created = UserShoppingCart.objects.prefetch_related(
            'recipes'
        ).get_or_create(user=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.can_add_to_shopping_cart(
                shopping_cart, recipe, raise_exception=True
        ):
            shopping_cart.recipes.add(recipe)

        context = {'request': request}
        serializer = self.get_serializer(
            recipe,
            context=context,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def can_add_to_shopping_cart(shopping_cart, recipe, raise_exception=True):
        if recipe in shopping_cart.recipes.all():
            if raise_exception:
                raise ValidationError(_('Cannot add to shopping cart twice.'))
            return False
        return True

    def remove_from_shopping_cart(self, request, pk=None):
        shopping_cart, created = UserShoppingCart.objects.prefetch_related(
            'recipes'
        ).get_or_create(user=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.can_remove_from_shopping_cart(
                shopping_cart, recipe, raise_exception=True
        ):
            shopping_cart.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def can_remove_from_shopping_cart(
            shopping_cart, recipe, raise_exception=True
    ):
        if recipe not in shopping_cart.recipes.all():
            if raise_exception:
                raise ValidationError(_('Not in shopping cart.'))
            return False
        return True

    @action(
        detail=False,
        methods=('get',),
        url_name='download-shopping-cart',
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart, created = UserShoppingCart.objects.get_or_create(
            user=user
        )
        ingredients = shopping_cart.get_ingredients_to_buy()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        pdfmetrics.registerFont(TTFont('DejaVu Serif', 'DejaVuSerif.ttf'))
        if ingredients:
            table = Table(
                ingredients,
                hAlign='LEFT',
                style=[
                    ('FONT', (0, 0), (-1, -1), 'DejaVu Serif'),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ]
            )
            doc.build([table])
        else:
            doc.build([Paragraph(_('Shopping cart is empty.'))])
        buffer.seek(0)

        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping_cart.pdf'
        )
