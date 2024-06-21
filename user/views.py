"""
user views
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserCreateSerializer, UserSerializer, ChangePasswordSerializer

User = get_user_model()


class UserCreateView(CreateAPIView):
    """
    user create view
    """

    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """
        perform create
        :param serializer:
        :return:
        """
        groups = Group.objects.filter(name=settings.DEFAULT_USER_GROUP).values_list(
            "id", flat=True
        )
        _user = serializer.save()
        _user.groups.add(*groups)


class UserView(RetrieveUpdateAPIView):
    """
    user view (Retrieve and Update)
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        """
        get object
        :return: user object
        """
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    """
    change password view
    """

    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    http_method_names = ["put"]

    def get_object(self):
        """
        get object
        :return: user object
        """
        return self.request.user
