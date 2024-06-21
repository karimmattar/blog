"""
User admin
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    User admin class
    """

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
