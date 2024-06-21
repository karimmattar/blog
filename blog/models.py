"""
Blog models
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStamp(models.Model):
    """
    Model representing a time stamp with created_at and updated_at fields.

    Attributes:
        created_at (models.DateTimeField): Date and time when the object was created.
        updated_at (models.DateTimeField): Date and time when the object was last updated.

    Meta:
        abstract (bool): Indicates that this model is abstract and should
        not be created in the database.
    """

    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        """
        abstract = True
        """

        abstract = True


class Slug(models.Model):
    """
    Model representing a slug with a name and slug field.

    Attributes:
        name (models.CharField): Name of the item.
        slug (models.SlugField): Slug field for the item.

    Meta:
        abstract (bool): Indicates that this model is abstract and should
        not be created in the database.
    """

    name = models.CharField(_("item name"), max_length=255, unique=True)
    slug = models.SlugField(_("item slug"), max_length=255, null=True, blank=True)

    class Meta:
        """
        abstract = True
        """

        abstract = True

    def save(self, *args, **kwargs):
        """
        save method for slug
        """
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Profile(TimeStamp):
    """
    Profile model

    Fields:
        user (models.OneToOneField): One-to-one relationship with the User model.
        bio (models.TextField): Text field for the user's biography.
        profile_picture (models.ImageField): Image field for the user's profile picture.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile",
        help_text=_("user object"),
    )
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pictures")


class Category(TimeStamp, Slug):
    """
    Category model

    Inherits from:
        - TimeStamp
        - Slug
    """

    class Meta:
        """
        Meta class for category model
        """

        ordering = ("name",)


class Tag(TimeStamp, Slug):
    """
    Tag model

    Inherits from:
        - TimeStamp
        - Slug
    """

    class Meta:
        """
        Meta class for tag model
        """

        ordering = ("name",)


class Post(TimeStamp):
    """
    Post model

    Fields:
        title (models.CharField): Title of the post.
        content (models.TextField): Content of the post.
        author (models.ForeignKey): Foreign key relationship with the Profile model.
        categories (models.ManyToManyField): Many-to-many relationship with the Category model.
        tags (models.ManyToManyField): Many-to-many relationship with the Tag model.
    """

    title = models.CharField(max_length=255)
    content = models.TextField(_("post content"), null=False, blank=False)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="author_posts",
        help_text=_("profile object"),
    )
    categories = models.ManyToManyField(
        Category,
        related_name="category_posts",
        help_text=_("category object"),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tag_posts",
        help_text=_("tag object"),
    )

    class Meta:
        """
        Meta class for post model
        """

        ordering = ("-created_at",)


class Comment(TimeStamp):
    """
    Comment model

    Fields:
        post (models.ForeignKey): Foreign key relationship with the Post model.
        author (models.ForeignKey): Foreign key relationship with the Profile model.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_comments",
        help_text=_("post object"),
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="author_comments",
        help_text=_("profile object"),
    )
    content = models.TextField(_("comment content"), null=False, blank=False)

    class Meta:
        """
        Meta class for comment model
        """

        ordering = ("-created_at",)
