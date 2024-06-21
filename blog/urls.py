"""
Blog urls
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    TagViewSet,
    PostViewSet,
    CommentViewSet,
    ProfileViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
urlpatterns.extend([path("profile/", ProfileViewSet.as_view(), name="profile")])
