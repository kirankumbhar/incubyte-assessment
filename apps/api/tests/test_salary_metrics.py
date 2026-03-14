import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
 
# api_client and create_employee fixtures are defined in conftest.py.
 
 
@pytest.mark.django_db
class TestSalaryMetricsByCountry:
    def test_returns_200_for_existing_country(self, api_client, create_employee):
        create_employee(country="India", salary=Decimal("80000.00"))
        url = reverse("salary-metrics-by-country") + "?country=India"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
 
    def test_returns_404_for_unknown_country(self, api_client):
        url = reverse("salary-metrics-by-country") + "?country=Narnia"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
 
    def test_returns_400_when_country_param_missing(self, api_client):
        url = reverse("salary-metrics-by-country")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
 
    def test_returns_correct_min_max_avg(self, api_client, create_employee):
        create_employee(country="India", salary=Decimal("50000.00"))
        create_employee(country="India", salary=Decimal("100000.00"))
        create_employee(country="India", salary=Decimal("150000.00"))
        url = reverse("salary-metrics-by-country") + "?country=India"
        response = api_client.get(url)
        data = response.json()
        assert Decimal(data["min_salary"]) == Decimal("50000.00")
        assert Decimal(data["max_salary"]) == Decimal("150000.00")
        assert Decimal(data["average_salary"]) == Decimal("100000.00")
 
    def test_returns_correct_country_in_response(self, api_client, create_employee):
        create_employee(country="India")
        url = reverse("salary-metrics-by-country") + "?country=India"
        response = api_client.get(url)
        assert response.json()["country"] == "India"
 
    def test_country_matching_is_case_insensitive(self, api_client, create_employee):
        create_employee(country="India", salary=Decimal("80000.00"))
        url = reverse("salary-metrics-by-country") + "?country=india"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
 
    def test_ignores_employees_from_other_countries(self, api_client, create_employee):
        create_employee(country="India", salary=Decimal("100000.00"))
        create_employee(country="United States", salary=Decimal("999999.00"))
        url = reverse("salary-metrics-by-country") + "?country=India"
        response = api_client.get(url)
        data = response.json()
        assert Decimal(data["max_salary"]) == Decimal("100000.00")
 
    def test_single_employee_min_max_avg_are_equal(self, api_client, create_employee):
        create_employee(country="India", salary=Decimal("75000.00"))
        url = reverse("salary-metrics-by-country") + "?country=India"
        response = api_client.get(url)
        data = response.json()
        assert data["min_salary"] == data["max_salary"] == data["average_salary"]
 
 
@pytest.mark.django_db
class TestSalaryMetricsByJobTitle:
    def test_returns_200_for_existing_job_title(self, api_client, create_employee):
        create_employee(job_title="Software Engineer")
        url = reverse("salary-metrics-by-job-title") + "?job_title=Software Engineer"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
 
    def test_returns_404_for_unknown_job_title(self, api_client):
        url = reverse("salary-metrics-by-job-title") + "?job_title=Astronaut"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
 
    def test_returns_400_when_job_title_param_missing(self, api_client):
        url = reverse("salary-metrics-by-job-title")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
 
    def test_returns_correct_average_salary(self, api_client, create_employee):
        create_employee(job_title="Software Engineer", salary=Decimal("80000.00"))
        create_employee(job_title="Software Engineer", salary=Decimal("120000.00"))
        url = reverse("salary-metrics-by-job-title") + "?job_title=Software Engineer"
        response = api_client.get(url)
        data = response.json()
        assert Decimal(data["average_salary"]) == Decimal("100000.00")
 
    def test_job_title_matching_is_case_insensitive(self, api_client, create_employee):
        create_employee(job_title="Software Engineer", salary=Decimal("100000.00"))
        url = reverse("salary-metrics-by-job-title") + "?job_title=software engineer"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
 
    def test_ignores_employees_with_different_job_titles(self, api_client, create_employee):
        create_employee(job_title="Software Engineer", salary=Decimal("100000.00"))
        create_employee(job_title="Manager", salary=Decimal("999999.00"))
        url = reverse("salary-metrics-by-job-title") + "?job_title=Software Engineer"
        response = api_client.get(url)
        data = response.json()
        assert Decimal(data["average_salary"]) == Decimal("100000.00")
 
    def test_returns_job_title_in_response(self, api_client, create_employee):
        create_employee(job_title="Software Engineer")
        url = reverse("salary-metrics-by-job-title") + "?job_title=Software Engineer"
        response = api_client.get(url)
        assert response.json()["job_title"] == "Software Engineer"