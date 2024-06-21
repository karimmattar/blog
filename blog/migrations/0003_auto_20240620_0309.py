# Generated by Django 5.0.6 on 2024-06-20 03:09

from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration class
    """

    dependencies = [
        ("blog", "0002_initial"),
    ]

    def seed_categories(apps, schema_editor):
        """
        Seed categories
        :param schema_editor:
        :return:
        """
        Category = apps.get_model("blog", "Category")
        categories = []
        for i in range(10):
            categories.append(Category(name=f"Category {i}", slug=f"category-{i}"))
        Category.objects.bulk_create(categories)

    def seed_tags(apps, schema_editor):
        """
        Seed tags
        :param schema_editor:
        :return:
        """
        Tag = apps.get_model("blog", "Tag")
        tags = []
        for i in range(10):
            tags.append(Tag(name=f"Tag {i}", slug=f"tag-{i}"))
        Tag.objects.bulk_create(tags)

    operations = [
        migrations.RunPython(seed_categories),
        migrations.RunPython(seed_tags),
    ]
