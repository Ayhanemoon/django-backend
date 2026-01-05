import pytest
from accounts.models import Address, User


@pytest.mark.django_db
def test_user_can_have_multiple_addresses():
    user = User.objects.create_user(
        email="test@example.com",
        password="password123",
    )

    Address.objects.create(
        user=user,
        title="Home",
        receiver_name="John Doe",
        phone_number="09120000000",
        state="Tehran",
        city="Tehran",
        postal_code="1234567890",
        address_line_1="Street 1",
        is_default=True,
    )

    Address.objects.create(
        user=user,
        title="Office",
        receiver_name="John Doe",
        phone_number="09120000000",
        state="Tehran",
        city="Tehran",
        postal_code="0987654321",
        address_line_1="Street 2",
    )

    assert user.addresses.count() == 2


@pytest.mark.django_db
def test_only_one_default_address_per_user():
    user = User.objects.create_user(
        email="test2@example.com",
        password="password123",
    )

    addr1 = Address.objects.create(
        user=user,
        title="Home",
        receiver_name="John",
        phone_number="0912",
        state="Tehran",
        city="Tehran",
        postal_code="111",
        address_line_1="Line 1",
        is_default=True,
    )

    addr2 = Address.objects.create(
        user=user,
        title="Office",
        receiver_name="John",
        phone_number="0912",
        state="Tehran",
        city="Tehran",
        postal_code="222",
        address_line_1="Line 2",
        is_default=True,
    )

    addr1.refresh_from_db()
    addr2.refresh_from_db()

    assert addr2.is_default is True
    assert addr1.is_default is False
