# Django Assessment — Senior SWE Technical Test

A TDD-first Django REST Framework scaffold using **Poetry**, **pytest**, **pytest-factoryboy**, and **flake8**.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Django 5 + DRF | Web framework & REST API |
| SQLite | Database (zero-config for local dev) |
| Poetry | Dependency & virtual-env management |
| pytest + pytest-django | Test runner |
| pytest-factoryboy | Factory-based fixtures from factory_boy |
| factory_boy + Faker | Realistic test data generation |
| flake8 | Linting & style enforcement |
| coverage / pytest-cov | Code coverage reporting |

---

## Project Structure

```
.
├── config/
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL config
│   └── wsgi.py
├── apps/
│   └── api/
│       ├── migrations/
│       ├── tests/
│       │   ├── factories.py       # factory_boy factories
│       │   ├── test_models.py     # Model unit tests
│       │   ├── test_serializers.py
│       │   └── test_views.py      # API integration tests
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── conftest.py            # Shared pytest fixtures + factory registration
├── manage.py
├── pyproject.toml         # Poetry config + pytest/coverage config
├── .flake8                # Linting rules
├── .env.example
└── .gitignore
```

---

## Step-by-Step Setup

### 1. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify:
```bash
poetry --version
```

### 2. Install dependencies

```bash
poetry install
```

This creates a `.venv` virtual environment and installs all dependencies.

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` if needed (defaults work fine for local dev).

### 4. Run database migrations

```bash
poetry run python manage.py migrate
```

### 5. (Optional) Create a superuser

```bash
poetry run python manage.py createsuperuser
```

### 6. Start the dev server

```bash
poetry run python manage.py runserver
```

API is available at: `http://127.0.0.1:8000/api/items/`

---

## Running Tests

### Run all tests with coverage

```bash
poetry run pytest
```

### Run a specific test file

```bash
poetry run pytest apps/api/tests/test_views.py
```

### Run a specific test class or method

```bash
poetry run pytest apps/api/tests/test_views.py::TestItemCreateAPI
poetry run pytest apps/api/tests/test_views.py::TestItemCreateAPI::test_create_returns_201
```

### Run without coverage (faster)

```bash
poetry run pytest --no-cov
```

### View HTML coverage report

```bash
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Linting

```bash
# Check for lint errors
poetry run flake8 .

# Check a specific file
poetry run flake8 apps/api/views.py
```

---

## API Endpoints

Base URL: `/api/`

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/items/` | List all items (paginated) |
| POST | `/api/items/` | Create a new item |
| GET | `/api/items/{id}/` | Retrieve a single item |
| PUT | `/api/items/{id}/` | Full update |
| PATCH | `/api/items/{id}/` | Partial update |
| DELETE | `/api/items/{id}/` | Delete |

### Query Params

| Param | Values | Description |
|---|---|---|
| `is_active` | `true` / `false` | Filter by active status |

### Example Request/Response

**POST /api/items/**
```json
// Request
{ "name": "Widget Pro", "description": "A great widget", "is_active": true }

// Response 201
{ "id": 1, "name": "Widget Pro", "description": "A great widget", "is_active": true, "created_at": "...", "updated_at": "..." }
```

---

## TDD Workflow

This scaffold is built for a **Red → Green → Refactor** cycle:

```
1. Write a failing test first (Red)
2. Write the minimum code to make it pass (Green)
3. Refactor without breaking tests (Refactor)
```

### Adding a new feature

1. Create / update the factory in `apps/api/tests/factories.py`
2. Write model tests in `test_models.py`
3. Write serializer tests in `test_serializers.py`
4. Write API/view tests in `test_views.py`
5. Implement model → serializer → view → urls
6. Run `poetry run pytest` — all tests should be green
7. Run `poetry run flake8 .` — no lint errors

---

## Adding a New App

```bash
poetry run python manage.py startapp <appname> apps/<appname>
```

Then in `config/settings.py`, add `"apps.<appname>"` to `LOCAL_APPS`.
