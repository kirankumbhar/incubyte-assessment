from decimal import Decimal
from django.db.models import Min, Max, Avg

from apps.api.models import Employee
 
DEDUCTION_RULES = {
    "india": Decimal("0.10"),
    "united states": Decimal("0.12"),
}
 
 
def calculate_salary(gross: Decimal, country: str) -> dict:
    """
    Pure function: returns gross, deductions dict, and net salary.
    No Django dependencies — fast and easy to unit test.
    """
    rate = DEDUCTION_RULES.get(country.strip().lower(), Decimal("0.00"))
    tds = (gross * rate).quantize(Decimal("0.01"))
 
    deductions = {"tds": tds} if tds > 0 else {}
    net = gross - tds
 
    return {
        "gross_salary": gross,
        "deductions": deductions,
        "net_salary": net,
    }
 
def get_metrics_by_country(country: str) -> dict:
    """Returns min, max, and average salary for all employees in a country."""
    qs = Employee.objects.filter(country__iexact=country)
    if not qs.exists():
        return None
 
    result = qs.aggregate(
        min_salary=Min("salary"),
        max_salary=Max("salary"),
        average_salary=Avg("salary"),
    )
    result["country"] = country
    return result
 
 
def get_avg_salary_by_job_title(job_title: str) -> dict:
    """Returns the average salary for all employees with a given job title."""
    qs = Employee.objects.filter(job_title__iexact=job_title)
    if not qs.exists():
        return None
 
    result = qs.aggregate(average_salary=Avg("salary"))
    result["job_title"] = job_title
    return result