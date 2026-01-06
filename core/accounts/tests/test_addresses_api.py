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
        Address.objects.create(profile=self.profile, title="Home", address_line_1="123", city="Tehran", postal_code="11111", country="Iran")
        Address.objects.create(profile=self.profile, title="Work", address_line_1="456", city="Tehran", postal_code="22222", country="Iran")

        url = reverse("accounts:api-v1:address-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        titles = [addr["title"] for addr in response.data]
        assert "Home" in titles
        assert "Work" in titles

    def test_retrieve_address(self):
        address = Address.objects.create(profile=self.profile, title="Home", address_line_1="123", city="Tehran", postal_code="11111", country="Iran")
        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Home"

    def test_update_address(self):
        address = Address.objects.create(profile=self.profile, title="Home", address_line_1="123", city="Tehran", postal_code="11111", country="Iran")
        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        data = {"title": "Updated Home"}
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        address.refresh_from_db()
        assert address.title == "Updated Home"

    def test_delete_address(self):
        address = Address.objects.create(profile=self.profile, title="Home", address_line_1="123", city="Tehran", postal_code="11111", country="Iran")
        url = reverse("accounts:api-v1:address-detail", args=[address.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Address.objects.filter(id=address.id).exists()

    def test_cannot_access_other_users_address(self):
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
        assert response.status_code == status.HTTP_404_NOT_FOUND  # because queryset filters by request.user
