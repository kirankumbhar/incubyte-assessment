import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def api_client():
    """Unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def auth_client(api_client, django_user_model):
    """
    Authenticated DRF test client.
    Creates a test user and forces authentication.
    """
    user = django_user_model.objects.create_user(
        username="testuser",
        password="testpassword123!",
    )
    api_client.force_authenticate(user=user)
    return api_client
