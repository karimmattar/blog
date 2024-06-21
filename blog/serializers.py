"""
Blog serializers
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Category, Tag, Comment, Profile

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        """
        Meta class for category serializer
        """

        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "slug")


class TagSerializer(serializers.ModelSerializer):
    """
    Tag serializer
    """

    class Meta:
        """
        Meta class for tag serializer
        """

        model = Tag
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "slug")


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer
    """

    categories = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="slug",
        queryset=Category.objects.all(),
        required=False,
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="slug",
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        """
        Meta class for post serializer
        """

        model = Post
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "author")


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment serializer
    """

    class Meta:
        """
        Meta class for comment serializer
        """

        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "author")


class UserManagerSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    class Meta:
        """
        Meta class for user serializer
        """

        model = User
        fields = ("first_name", "last_name")


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer
    """

    user = serializers.StringRelatedField(read_only=True, source="user.email")

    class Meta:
        """
        Meta class for profile serializer
        """

        model = Profile
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "user")
