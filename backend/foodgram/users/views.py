from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import User


class UserViewSet(DjoserUserViewSet):
    def get_permissions(self):
        if self.action == 'subscriptions':
            self.permission_classes = settings.PERMISSIONS.get_subscriptions
        elif self.action == 'subscribe':
            self.permission_classes = settings.PERMISSIONS.subscribe
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return settings.SERIALIZERS.get_subscriptions
        elif self.action == 'subscribe':
            return settings.SERIALIZERS.subscribe
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=('get',),
    )
    def subscriptions(self, request):
        current_user = request.user
        queryset = current_user.follows.all()
        context = {'request': request}
        serializer = self.get_serializer(
            queryset,
            context=context,
            many=True,
        )
        self.paginate_queryset(queryset)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('get', 'delete'),
    )
    def subscribe(self, request, id=None):
        operation = {
            'GET': self.create_subscription,
            'DELETE': self.destroy_subscription,
        }
        return operation[request.method](request, id)

    def create_subscription(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)

        if self.is_valid_subscription(user, following, raise_exception=True):
            user.follows.add(following)

        context = {'request': request}
        serializer = self.get_serializer(
            following,
            context=context,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def is_valid_subscription(user, following, raise_exception=True):
        if user == following:
            if raise_exception:
                raise ValidationError('Self follows are forbidden.')
            return False
        if following in user.follows.all():
            if raise_exception:
                raise ValidationError('Cannot follow twice.')
            return False
        return True

    def destroy_subscription(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)

        if self.is_destroyable_subscription(
                user, following, raise_exception=True
        ):
            user.follows.remove(following)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def is_destroyable_subscription(user, following, raise_exception=True):
        if following not in user.follows.all():
            if raise_exception:
                raise ValidationError('Subscription not existed.')
            return False
        return True
