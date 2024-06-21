"""
Blog views
"""

from guardian.shortcuts import assign_perm
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoObjectPermissions

from .models import Category, Tag, Post, Profile, Comment
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostSerializer,
    CommentSerializer,
    ProfileSerializer,
)


class CategoryViewSet(ModelViewSet):
    """
    List retrieve category view
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filterset_fields = ("slug",)
    lookup_field = "id"
    http_method_names = ["get"]


class TagViewSet(ModelViewSet):
    """
    List retrieve tag view
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filterset_fields = ("slug",)
    lookup_field = "id"
    http_method_names = ["get"]


class WithPermissionsMixin:
    """
    With permissions mixin
    """

    model = None
    request = None

    def __init__(self, *args, **kwargs):
        """
        Initialize
        :param args:
        :param kwargs:
        """
        if not hasattr(self, "model") or getattr(self, "model") is None:
            raise AttributeError("WithPermissionsViewSet must have a model attribute")

        if not hasattr(self, "request") or getattr(self, "request") is None:
            raise AttributeError("WithPermissionsViewSet must have a request attribute")
        super().__init__(*args, **kwargs)

    def assign_permissions(self, _object):
        """
        Assign permissions to object
        :param _object:
        :return:
        """
        assign_perm(
            "change_%s" % self.model.__name__.lower(), self.request.user, _object
        )
        assign_perm(
            "delete_%s" % self.model.__name__.lower(), self.request.user, _object
        )


class PostViewSet(ModelViewSet, WithPermissionsMixin):
    """
    List, Retrieve, Update, Destroy and Create post view
    """

    permission_classes = (DjangoObjectPermissions,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    model = Post
    search_fields = ("title", "content")
    lookup_field = "id"

    def perform_create(self, serializer):
        """
        Override perform_create method for post creation
        :param serializer:
        :return:
        """
        _user = self.request.user
        author, _ = Profile.objects.get_or_create(user=_user)
        _object = serializer.save(author=author)
        self.assign_permissions(_object)


class CommentViewSet(ModelViewSet, WithPermissionsMixin):
    """
    List, Retrieve, Update, Destroy and Create comment view
    """

    permission_classes = (DjangoObjectPermissions,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    model = Comment
    lookup_field = "id"
    http_method_names = ["get", "post", "delete"]

    def perform_create(self, serializer):
        """
        Override perform_create method for post creation
        :param serializer:
        :return:
        """
        _user = self.request.user
        author, _ = Profile.objects.get_or_create(user=_user)
        _object = serializer.save(author=author)
        self.assign_permissions(_object)


class ProfileViewSet(RetrieveUpdateAPIView, WithPermissionsMixin):
    """
    Retrieve, Update profile view
    """

    permission_classes = (DjangoObjectPermissions,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    model = Profile

    def get_object(self):
        """
        Override get_object method
        :return:
        """
        _user = self.request.user
        profile, _ = Profile.objects.get_or_create(user=_user)
        return profile
