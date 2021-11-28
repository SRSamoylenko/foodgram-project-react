from django.urls import include, path

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('', include('recipes.urls', namespace='recipes')),
    path('auth/', include('djoser.urls.authtoken')),
]
