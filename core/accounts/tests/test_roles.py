import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command


@pytest.mark.django_db
def test_setup_roles_command():
    call_command("setup_roles")

    admin = Group.objects.get(name="Admin")
    accountant = Group.objects.get(name="Accountant")
    operator = Group.objects.get(name="Operator")

    assert admin.permissions.count() > 0
    assert accountant.permissions.count() > 0
    assert operator.permissions.count() > 0
