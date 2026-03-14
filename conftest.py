import pytest
from pytest_factoryboy import register
from decimal import Decimal
from rest_framework.test import APIClient
from apps.api.models import Employee


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def api_client(db):
    """Unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def auth_client(db, api_client, django_user_model):
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


@pytest.fixture
def employee_payload():
    return {
        "full_name": "Jane Doe",
        "job_title": "Software Engineer",
        "country": "India",
        "salary": "100000.00",
    }


@pytest.fixture
def create_employee(db):
    def _create(**kwargs):
        defaults = {
            "full_name": "Test User",
            "job_title": "Developer",
            "country": "India",
            "salary": Decimal("80000.00"),
        }
        defaults.update(kwargs)
        return Employee.objects.create(**defaults)
    return _create