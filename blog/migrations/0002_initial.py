# Generated by Django 5.0.6 on 2024-06-20 03:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                help_text="user object",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                help_text="profile object",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author_posts",
                to="blog.profile",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                help_text="profile object",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author_comments",
                to="blog.profile",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                help_text="tag object", related_name="tag_posts", to="blog.tag"
            ),
        ),
    ]