from django.urls import reverse
from rest_framework.test import APIClient
import pytest
from shop.orders.models import Order
from accounts.models import User, Profile, Address


@pytest.mark.django_db
class TestOrdersAPI:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@tset.com",
            password="test@1234567",
            is_verified=True,
            is_active=True,
        )
        self.profile = Profile.objects.get(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.address = Address.objects.create(
            profile=self.profile,
            title="Home",
            address_line_1="123 Main St",
            city="Tehran",
            state="Tehran",
            postal_code="11111",
            country="Iran",
            is_default=True
        )

    def test_create_order(self):
        url = reverse("orders:api-v1:order-list")
        data = {
            "profile": self.profile.id,
        }
        response = self.client.post(url, data)
        assert response.status_code == 201
        assert Order.objects.filter(profile=self.profile).exists()

    def test_get_order_list(self):
        Order.objects.create(profile=self.profile)
        url = reverse("orders:api-v1:order-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) > 0
