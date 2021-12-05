from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Follow, User

EMPTY_VALUE_MESSAGE = _('-empty-')


class FollowInLine(admin.TabularInline):
    fk_name = 'from_user'
    model = Follow
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'username',
    )
    inlines = (FollowInLine,)
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
