from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from listing.models import Listing


class Command(BaseCommand):
    help = "Создание групп пользователей и назначение разрешений"

    def handle(self, *args, **options):
        permissions_by_group = {
            "admin": [
                "add_listing",
                "change_listing",
                "delete_listing",
                "view_listing",
                "can_moderate_listing",
                "can_moderate_self_listing",
            ],
            "moderator": [
                "add_listing",
                "change_listing",
                "view_listing",
                "can_moderate_listing",
            ],
            "user": [
                "add_listing",
                "change_listing",
                "delete_listing",
                "view_listing",
                "can_moderate_self_listing",
            ],
        }

        content_type = ContentType.objects.get_for_model(Listing)

        for group_name, codenames in permissions_by_group.items():
            group, created = Group.objects.get_or_create(
                name=group_name
            )

            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=codenames,
            )

            group.permissions.set(permissions)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Группа {group_name} создана."
                    )
                )
            else:
                self.stdout.write(
                    f"Группа {group_name} обновлена."
                )

        self.stdout.write(
            self.style.SUCCESS("Группы и разрешения настроены.")
        )

