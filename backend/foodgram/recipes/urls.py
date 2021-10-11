from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'tags',
    TagViewSet,
    basename='tag',
)
router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredient',
)
router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipe',
)

urlpatterns = router.urls

