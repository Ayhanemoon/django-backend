from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


ROLE_PERMISSIONS = {
    "Admin": ["*"],  # Admin gets all permissions
    "Accountant": [
        "view_order",
        "change_order",
        "view_payment",
        "view_product",
    ],
    "Operator": [
        "view_order",
        "change_order",
        "view_product",
    ],
    "Blog Writer": [
        "add_post",
        "change_post",
        "delete_post",
        "view_post",
        "add_category",
        "change_category",
        "delete_category",
        "view_category",
    ],
}


class Command(BaseCommand):
    help = "Setup operational staff groups and assign permissions"

    def handle(self, *args, **options):
        for role_name, perms in ROLE_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=role_name)
            self.stdout.write(f"{'Created' if created else 'Exists'} group: {role_name}")

            permissions_to_assign = []

            if "*" in perms:
                # Admin: assign all permissions
                permissions_to_assign = Permission.objects.all()
            else:
                for perm_codename in perms:
                    try:
                        perm = Permission.objects.get(codename=perm_codename)
                        permissions_to_assign.append(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            f"WARNING: Permission {perm_codename} does not exist yet, skipping."
                        )

            group.permissions.set(permissions_to_assign)
            group.save()
            self.stdout.write(
                self.style.SUCCESS(f"Permissions assigned to {role_name}")
            )
