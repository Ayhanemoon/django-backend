import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User, Profile, Address


@pytest.mark.django_db
class TestAddressAPI:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.client = APIClient()
        # Create a verified user
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test@1234567",
            is_verified=True,
            is_active=True,
        )
        self.profile = Profile.objects.get(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_address(self):
        url = reverse("accounts:api-v1:address-list")  # ViewSet name -> basename-list
        data = {
            "title": "Home",
            "receiver_name": "John Doe",
            "phone_number": "09120000000",
            "state": "Tehran",
            "city": "Tehran",
            "postal_code": "11111",
            "address_line_1": "123",
            "country": "Iran",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Address.objects.filter(profile=self.profile, title="Home").exists()

    def test_list_addresses(self):
        # Pre-create some addresses
        Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )
        Address.objects.create(
            profile=self.profile,
            title="Work",
            address_line_1="456",
            city="Tehran",
            postal_code="22222",
            country="Iran",
        )

        url = reverse("accounts:api-v1:address-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        titles = [addr["title"] for addr in response.data]
        assert "Home" in titles
        assert "Work" in titles

    def test_retrieve_address(self):
        address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )
        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Home"

    def test_update_address(self):
        address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )
        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        data = {"title": "Updated Home"}
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        address.refresh_from_db()
        assert address.title == "Updated Home"

    def test_delete_address(self):
        address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )

        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        address.refresh_from_db()
        assert address.deleted_at is not None
        assert not Address.objects.alive().filter(id=address.id).exists()

    """def test_cannot_access_other_users_address(self):
        other_user = User.objects.create_user(
            email="user@example.com",
            password="example@1234567",
            is_verified=True,
            is_active=True,
        )
        other_profile = Profile.objects.get(user=other_user)
        other_address = Address.objects.create(profile=other_profile, title="Other", address_line_1="999", city="Tehran", postal_code="99999", country="Iran")
        url = reverse("accounts:api-v1:address-detail", args=[other_address.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND  # because queryset filters by request.user"""

    def test_cannot_update_other_users_address(self):
        other_user = User.objects.create_user(
            email="other@example.com", password="pass"
        )
        other_profile = Profile.objects.get(user=other_user)
        address = Address.objects.create(
            profile=other_profile,
            title="Other",
            receiver_name="Someone",
            phone_number="09123456789",
            state="Tehran",
            city="Tehran",
            postal_code="00000",
            address_line_1="Line",
        )

        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        data = {"title": "Hacked"}
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN  # Forbidden

    def test_get_default_address(self):
        # Create two addresses, only one default
        Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
            is_default=False,
        )
        addr2 = Address.objects.create(
            profile=self.profile,
            title="Office",
            address_line_1="456",
            city="Tehran",
            postal_code="22222",
            country="Iran",
            is_default=True,
        )

        url = reverse(
            "accounts:api-v1:address-default-address"
        )  # matches @action url_path
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == addr2.id
        assert response.data["is_default"] is True

    def test_delete_address_is_soft_delete(self):
        address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )

        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        response = self.client.delete(url)

        address.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert address.deleted_at is not None

    def test_deleted_address_not_listed(self):
        address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )
        address.soft_delete()

        url = reverse("accounts:api-v1:address-list")
        response = self.client.get(url)

        assert len(response.data) == 0

    def test_deleted_address_not_retrievable(self):
        address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123",
            city="Tehran",
            postal_code="11111",
            country="Iran",
        )
        address.soft_delete()

        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
