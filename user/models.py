"""
This file contains custom model for user.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model representing a user with email as the unique identifier.

    Attributes:
        validate_email (EmailValidator): Validator for email field.
        email (models.EmailField): Email address of the user.
        USERNAME_FIELD (str): Field used as the unique identifier for the user.
        REQUIRED_FIELDS (list): List of fields required when creating a user.
    """

    validate_email = EmailValidator(message="Please enter a valid email address")
    email = models.EmailField(
        _("email address"), max_length=255, unique=True, validators=[validate_email]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
