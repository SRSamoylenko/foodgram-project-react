from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow
from .validators import IsCreatedValidator

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_subscribed',
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj in user.following.all()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('from_user', 'to_user')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['from_user', 'to_user'],
                message=_('Double follows are forbidden.'),
            ),
        )

    def validate(self, data):
        if data['from_user'] == data['to_user']:
            raise serializers.ValidationError(_('Self follows are forbidden.'))
        return data


class FollowDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('from_user', 'to_user')
        validators = (
            IsCreatedValidator(
                queryset=Follow.objects.all(),
                fields=['from_user', 'to_user'],
                message=_('Follow does not exist.')
            ),
        )

    def destroy(self):
        follow = Follow.objects.get(
            **self.validated_data
        )
        follow.delete()
