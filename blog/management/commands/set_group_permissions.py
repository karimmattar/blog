"""
Blog command to set group permissions
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """
    Command to set group permissions
    """

    help = "Create group permissions"

    def add_arguments(self, parser):
        """
        Add arguments
        :param parser:
        :return:
        """

    def handle(self, *args, **options):
        """
        Handle command
        :param args:
        :param options:
        :return:
        """
        name = settings.DEFAULT_USER_GROUP
        if Group.objects.filter(name=name).exists():
            raise CommandError("Group %s already exists" % name)

        group = Group.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS('Successfully created group "%s"' % name))

        group_permissions = Permission.objects.filter(
            codename__in=[
                "view_profile",
                "add_profile",
                "change_profile",
                "delete_profile",
                "view_post",
                "add_post",
                "change_post",
                "delete_post",
                "view_comment",
                "add_comment",
                "change_comment",
                "delete_comment",
            ]
        ).values_list("id", flat=True)
        group.permissions.add(*group_permissions)
        self.stdout.write(
            self.style.SUCCESS('Successfully added permissions to group "%s"' % name)
        )
