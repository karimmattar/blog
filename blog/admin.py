from django.contrib import admin

from .models import Post, Category, Comment, Tag, Profile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = (
        "id",
        "name",
    )
    search_fields = (
        "name",
        "slug",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = (
        "id",
        "name",
    )
    search_fields = (
        "name",
        "slug",
    )


class CommentInline(admin.TabularInline):
    """
    Comment inline
    """

    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = (
        "title",
        "content",
    )

    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = (
        "post",
        "author",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "bio",
    )
    list_display_links = ("id",)
    search_fields = (
        "user",
        "bio",
    )
