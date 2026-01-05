from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


ROLE_PERMISSIONS = {
    "Admin": ["*"],  # wildcard = all permissions
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
}


class Command(BaseCommand):
    help = "Setup operational staff groups and assign permissions"

    def handle(self, *args, **options):
        for role_name, perms in ROLE_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=role_name)
            self.stdout.write(f"{'Created' if created else 'Exists'} group: {role_name}")

            if "*" in perms:
                permissions = Permission.objects.all()
            else:
                permissions = []
                for perm_codename in perms:
                    try:
                        perm = Permission.objects.get(codename=perm_codename)
                        permissions.append(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            f"WARNING: Permission {perm_codename} does not exist yet."
                        )

            group.permissions.set(permissions)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Permissions assigned to {role_name}"))
