from django.contrib import admin

from .models import Post, Category, Comment, Tag, Profile

admin.site.register(Post)


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
