# Incubyte Salary Management

A production-ready Django REST Framework API for managing employees and computing salary deductions and metrics.

---

## Tech Stack

| Tool                     | Purpose                               |
| ------------------------ | ------------------------------------- |
| Django 5 + DRF           | Web framework & REST API              |
| SQLite                   | Zero-config local database            |
| Poetry                   | Dependency & virtual-env management   |
| pytest + pytest-django   | Test runner & Django integration      |
| factory_boy + Faker      | Realistic test data generation        |
| DRF Token Authentication | Built-in API auth, no extra libraries |
| flake8                   | Linting & style enforcement           |
| pytest-cov               | Code coverage reporting               |
| drf-spectacular          | Auto-generated OpenAPI/Swagger docs   |

---

## Project Structure

```
.
├── config/
│   ├── __init__.py
│   ├── settings.py          # Single settings file
│   ├── urls.py              # Root URL config
│   └── wsgi.py
├── apps/
│   └── employees/
│       ├── migrations/
│       ├── tests/
│       │   ├── test_models.py
│       │   ├── test_employee_crud.py
│       │   ├── test_salary_calculation.py
│       │   └── test_salary_metrics.py
│       ├── services/
│       │   ├── salary_calculator.py   # Pure function, no Django deps
│       │   └── salary_metrics.py      # ORM aggregations
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── conftest.py              # Shared pytest fixtures (api_client, auth_client, create_employee)
├── manage.py
├── pyproject.toml           # Poetry config + pytest/coverage settings
├── .flake8
├── .env.example
└── .gitignore
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- Poetry — install if not already present:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Steps

```bash

# 1. Install dependencies (creates .venv automatically)
poetry install

# 2. Copy environment variables
cp .env.example .env

# 3. Apply migrations
poetry run python manage.py migrate

# 4. Create a superuser (needed to obtain an auth token)
poetry run python manage.py createsuperuser

# 5. Start the dev server
poetry run python manage.py runserver
```

API is available at `http://127.0.0.1:8000/api/`

---

## Authentication

All endpoints require a token. First obtain one:

```bash
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin"
}
```

Response:

```json
{ "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }
```

Then pass it in every request header:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Running Tests

```bash
poetry run pytest
```

---

## Linting

````bash
# Check all files
poetry run flake8 .

---

### Endpoints Summary

| Method | URL                                            | Description                       |
| ------ | ---------------------------------------------- | --------------------------------- |
| POST   | `/api/auth/login/`                             | Obtain auth token                 |
| GET    | `/api/employees/`                              | List all employees                |
| POST   | `/api/employees/`                              | Create a new employee             |
| GET    | `/api/employees/{id}/`                         | Retrieve an employee              |
| PUT    | `/api/employees/{id}/`                         | Full update                       |
| PATCH  | `/api/employees/{id}/`                         | Partial update                    |
| DELETE | `/api/employees/{id}/`                         | Delete                            |
| GET    | `/api/employees/{id}/salary/`                  | Calculate net salary + deductions |
| GET    | `/api/salary-metrics/by-country/?country=`     | Min / max / avg salary by country |
| GET    | `/api/salary-metrics/by-job-title/?job_title=` | Average salary by job title       |

### Example Requests

**Create Employee**

```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Jane Doe", "job_title": "Software Engineer", "country": "India", "salary": "100000.00"}'
````

**Get Salary Calculation**

```bash
curl http://localhost:8000/api/employees/1/salary/ \
  -H "Authorization: Token <your_token>"
```

Response:

```json
{
  "employee_id": 1,
  "full_name": "Jane Doe",
  "country": "India",
  "gross_salary": "100000.00",
  "deductions": { "tds": "10000.00" },
  "net_salary": "90000.00"
}
```

**Salary Metrics by Country**

```bash
curl "http://localhost:8000/api/salary-metrics/by-country/?country=India" \
  -H "Authorization: Token <your_token>"
```

Response:

```json
{
  "country": "India",
  "min_salary": "50000.00",
  "max_salary": "200000.00",
  "average_salary": "125000.00"
}
```

**Salary Metrics by Job Title**

```bash
curl "http://localhost:8000/api/salary-metrics/by-job-title/?job_title=Software Engineer" \
  -H "Authorization: Token <your_token>"
```

Response:

```json
{
  "job_title": "Software Engineer",
  "average_salary": "120000.00"
}
```

---

## Deduction Rules

| Country       | Rule                        |
| ------------- | --------------------------- |
| India         | TDS = 10% of gross salary   |
| United States | TDS = 12% of gross salary   |
| All others    | No deductions — net = gross |

Country matching is case-insensitive.

---

## Design Decisions

**Service layer** — business logic lives in `apps/employees/services/`, fully decoupled from views. `salary_calculator.py` is a pure function with zero Django imports, making it trivially unit-testable without any HTTP or ORM overhead. `salary_metrics.py` uses Django ORM aggregations (`Min`, `Max`, `Avg`).s

**Built-in Token Auth** — uses DRF's `rest_framework.authtoken` rather than a third-party JWT library, keeping dependencies minimal for an API of this scope.

---

## Implementation Details — AI Usage

| Step                 | Tool               | How It Was Used                                                                                                                                          |
| -------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project scaffolding  | Claude (claude.ai) | Generated directory structure, boilerplate settings, urls, wsgi                                                                                          |
| Test case generation | Claude (claude.ai) | Enumerated edge cases per endpoint — missing fields, 404s, case sensitivity, boundary values, DB persistence checks — then reviewed and refined manually |
| Service logic        | Claude (claude.ai) | Drafted `calculate_salary` pure function; reviewed deduction rule mapping and decimal precision                                                          |
| Auth setup           | Claude (claude.ai) | Advised on DRF built-in token auth over JWT for minimal dependencies                                                                                     |
| Debugging            | Claude (claude.ai) | Diagnosed test isolation issue — missing `TEST: {NAME: ":memory:"}` in DATABASES causing rows to persist across tests                                    |
| README               | Claude (claude.ai) | Drafted structure and examples; reviewed and updated to match actual project setup                                                                       |

All AI-generated output was reviewed, adjusted for correctness, and integrated deliberately — not copy-pasted blindly.
