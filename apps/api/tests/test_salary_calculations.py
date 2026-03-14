import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from apps.api.models import Employee

 
 
@pytest.mark.django_db
class TestSalaryCalculationEndpoint:
    def test_returns_200_for_valid_employee(self, auth_client, create_employee):
        employee = create_employee()
        url = reverse("employee-salary", kwargs={"pk": employee.id})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
 
    def test_returns_404_for_missing_employee(self, auth_client):
        url = reverse("employee-salary", kwargs={"pk": 9999})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
 
    def test_india_employee_deduction_is_10_percent(self, auth_client, create_employee):
        employee = create_employee(country="India", salary=Decimal("100000.00"))
        url = reverse("employee-salary", kwargs={"pk": employee.id})
        response = auth_client.get(url)
        data = response.json()
        assert data["deductions"]["tds"] == "10000.00"
        assert data["net_salary"] == "90000.00"
        assert data["gross_salary"] == "100000.00"
 
    def test_us_employee_deduction_is_12_percent(self, auth_client, create_employee):
        employee = create_employee(country="United States", salary=Decimal("100000.00"))
        url = reverse("employee-salary", kwargs={"pk": employee.id})
        response = auth_client.get(url)
        data = response.json()
        assert data["deductions"]["tds"] == "12000.00"
        assert data["net_salary"] == "88000.00"
 
    def test_other_country_has_no_deductions(self, auth_client, create_employee):
        employee = create_employee(country="Germany", salary=Decimal("100000.00"))
        url = reverse("employee-salary", kwargs={"pk": employee.id})
        response = auth_client.get(url)
        data = response.json()
        assert data["deductions"] == {}
        assert data["net_salary"] == "100000.00"
 
    def test_response_contains_employee_info(self, auth_client, create_employee):
        employee = create_employee(full_name="Jane Doe", country="India")
        url = reverse("employee-salary", kwargs={"pk": employee.id})
        response = auth_client.get(url)
        data = response.json()
        assert data["employee_id"] == employee.id
        assert data["full_name"] == "Jane Doe"
        assert data["country"] == "India"