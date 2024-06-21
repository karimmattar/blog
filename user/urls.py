"""
user app urls
"""

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

from .views import UserCreateView, UserView, ChangePasswordView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("me/", UserView.as_view(), name="user_retrieve_update"),
    path(
        "me/password/",
        ChangePasswordView.as_view(),
        name="user_change_password",
    ),
]
