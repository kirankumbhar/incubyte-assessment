import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.api.models import Employee



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


@pytest.mark.django_db
class TestEmployeeCreate:
    def test_create_employee_returns_201(self, auth_client, employee_payload):
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_employee_persists_to_db(self, auth_client, employee_payload):
        url = reverse("employee-list")
        auth_client.post(url, employee_payload, format="json")
        assert Employee.objects.count() == 1

    def test_create_employee_returns_correct_data(self, auth_client, employee_payload):
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        data = response.json()
        assert data["full_name"] == "Jane Doe"
        assert data["job_title"] == "Software Engineer"
        assert data["country"] == "India"
        assert data["salary"] == "100000.00"
        assert "id" in data

    def test_create_employee_missing_full_name_returns_400(self, auth_client, employee_payload):
        del employee_payload["full_name"]
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "full_name" in response.json()

    def test_create_employee_missing_job_title_returns_400(self, auth_client, employee_payload):
        del employee_payload["job_title"]
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "job_title" in response.json()

    def test_create_employee_missing_country_returns_400(self, auth_client, employee_payload):
        del employee_payload["country"]
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "country" in response.json()

    def test_create_employee_missing_salary_returns_400(self, auth_client, employee_payload):
        del employee_payload["salary"]
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "salary" in response.json()

    def test_create_employee_negative_salary_returns_400(self, auth_client, employee_payload):
        employee_payload["salary"] = "-500.00"
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_employee_non_numeric_salary_returns_400(self, auth_client, employee_payload):
        employee_payload["salary"] = "abc"
        url = reverse("employee-list")
        response = auth_client.post(url, employee_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEmployeeList:
    def test_list_returns_200(self, auth_client):
        url = reverse("employee-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_returns_all_employees(self, auth_client, create_employee):
        create_employee(full_name="Alice")
        create_employee(full_name="Bob")
        url = reverse("employee-list")
        response = auth_client.get(url)
        assert len(response.json()) == 2

    def test_list_returns_empty_list_when_no_employees(self, auth_client):
        url = reverse("employee-list")
        response = auth_client.get(url)
        assert response.json() == []


@pytest.mark.django_db
class TestEmployeeRetrieve:
    def test_retrieve_existing_employee_returns_200(self, auth_client, create_employee):
        employee = create_employee()
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == employee.id

    def test_retrieve_nonexistent_employee_returns_404(self, auth_client):
        url = reverse("employee-detail", kwargs={"pk": 9999})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestEmployeeUpdate:
    def test_full_update_returns_200(self, auth_client, create_employee):
        employee = create_employee()
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        payload = {
            "full_name": "Updated Name",
            "job_title": "Senior Engineer",
            "country": "United States",
            "salary": "200000.00",
        }
        response = auth_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["full_name"] == "Updated Name"

    def test_partial_update_returns_200(self, auth_client, create_employee):
        employee = create_employee()
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        response = auth_client.patch(url, {"salary": "999999.00"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["salary"] == "999999.00"

    def test_update_nonexistent_employee_returns_404(self, auth_client):
        url = reverse("employee-detail", kwargs={"pk": 9999})
        response = auth_client.put(url, {}, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestEmployeeDelete:
    def test_delete_existing_employee_returns_204(self, auth_client, create_employee):
        employee = create_employee()
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_removes_employee_from_db(self, auth_client, create_employee):
        employee = create_employee()
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        auth_client.delete(url)
        assert Employee.objects.filter(id=employee.id).count() == 0

    def test_delete_nonexistent_employee_returns_404(self, auth_client):
        url = reverse("employee-detail", kwargs={"pk": 9999})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND