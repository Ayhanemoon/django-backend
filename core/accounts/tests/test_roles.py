import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command


@pytest.mark.django_db
def test_setup_roles_groups_exist():
    call_command("setup_roles")

    for role in ["Admin", "Accountant", "Operator"]:
        g = Group.objects.get(name=role)
        assert g is not None
