"""
user serializers
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        """
        model and fields for user creation
        """

        model = User
        fields = ("id", "email", "username", "password")
        extra_kwargs = {"id": {"read_only": True}, "username": {"read_only": True}}

    def validate_password(self, password):
        """
        validate password
        :param password:
        :return: password
        """
        try:
            validate_password(password)
        except Exception as errors:
            raise serializers.ValidationError(list(errors))
        return password

    def create(self, validated_data):
        """
        create method for user creation
        :param validated_data:
        :return: user object
        """
        _password = validated_data.pop("password")
        try:
            _username = validated_data["email"].split("@")[0]
            user = User(**validated_data, username=_username)
        except Exception as errors:
            raise serializers.ValidationError(list(errors))
        user.set_password(_password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user.
    """

    class Meta:
        """
        model and fields for user
        """

        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
        read_only_fields = ("id", "username", "last_login", "date_joined")

    def update(self, instance, validated_data):
        """
        update method for user
        :param instance:
        :param validated_data:
        :return: user object
        """
        _email = validated_data.get("email", None)
        if _email:
            if User.objects.filter(email=_email).exclude(id=instance.id).exists():
                raise serializers.ValidationError({"email": "Email already exists."})
            validated_data["username"] = _email.split("@")[0]
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for changing password
    """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        """
        model and fields for changing password
        """

        model = User
        fields = ("old_password", "new_password")

    def validate_new_password(self, password):
        """
        validate password
        :param password:
        :return: password
        """
        try:
            validate_password(password)
        except Exception as errors:
            raise serializers.ValidationError(list(errors))
        return password

    def update(self, instance, validated_data):
        """
        update method for changing password
        :param instance:
        :param validated_data:
        :return: user object
        """
        _old_password = validated_data.pop("old_password")
        _new_password = validated_data.pop("new_password")
        if not instance.check_password(_old_password):
            raise serializers.ValidationError({"old_password": "Wrong password."})
        instance.set_password(_new_password)
        instance.save()
        return instance
