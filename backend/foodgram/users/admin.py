from django.contrib import admin

from .models import User
from .constants import EMPTY_VALUE_MESSAGE


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE
