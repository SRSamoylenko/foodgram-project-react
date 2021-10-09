from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, Follow

EMPTY_VALUE_MESSAGE = _('-empty-')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'from_user',
        'to_user',
    )
    list_filter = (
        'from_user',
        'to_user',
    )
    empty_value_display = EMPTY_VALUE_MESSAGE
