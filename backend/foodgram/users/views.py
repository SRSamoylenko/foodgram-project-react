from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, FollowSerializer, FollowDestroySerializer
from .models import User
from rest_framework.response import Response


class UserViewSet(DjoserUserViewSet):
    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        current_user = request.user
        queryset = current_user.following.all()
        context = {'request': request}
        serializer = UserSerializer(
            queryset,
            context=context,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('get', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        operation = {
            'GET': self.create_subscription,
            'DELETE': self.destroy_subscription,
        }
        return operation[request.method](request, id)

    @staticmethod
    def create_subscription(request, id=None):
        from_user = request.user
        to_user = get_object_or_404(User, id=id)
        data = {
            'from_user': from_user.id,
            'to_user': to_user.id,
        }
        follow_serializer = FollowSerializer(
            data=data,
        )
        if follow_serializer.is_valid(raise_exception=True):
            follow_serializer.save()

        context = {'request': request}
        user_serializer = UserSerializer(
            to_user,
            context=context,
        )
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def destroy_subscription(request, id=None):
        from_user = request.user
        to_user = get_object_or_404(User, id=id)
        data = {
            'from_user': from_user.id,
            'to_user': to_user.id,
        }
        follow_serializer = FollowDestroySerializer(
            data=data,
        )
        if follow_serializer.is_valid(raise_exception=True):
            follow_serializer.destroy()
        return Response(status=status.HTTP_204_NO_CONTENT)
