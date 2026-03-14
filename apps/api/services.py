from decimal import Decimal
 
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