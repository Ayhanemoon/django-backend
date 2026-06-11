import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command


@pytest.mark.django_db
def test_setup_roles_groups_exist():
    """
    Test that the setup_roles command creates all staff groups
    and assigns permissions where they exist.
    """
    call_command("setup_roles")

    # List of expected groups
    expected_groups = ["Admin", "Accountant", "Operator", "Blog Writer"]

    for role in expected_groups:
        g = Group.objects.get(name=role)
        assert g is not None, f"{role} group should exist"

    # Blog Writer should only have Post/Category permissions (if they exist)
    blog_writer = Group.objects.get(name="Blog Writer")
    for perm in blog_writer.permissions.all():
        assert (
            perm.content_type.app_label == "blog"
        ), f"Blog Writer should only have blog permissions, found {perm}"
