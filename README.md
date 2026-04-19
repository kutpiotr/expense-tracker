# Expense Tracker

A full-stack personal finance application for tracking expenses, managing
categories, and visualizing spending habits. Built as a portfolio project to
demonstrate proficiency in Python/Flask, Vue 3, SQL, and REST API design.

![Dashboard overview](docs/screenshots/dashboard.png)

## Tech stack

**Backend** Python 3.14 · Flask · SQLAlchemy · Flask-Migrate · Pydantic
**Frontend** Vue 3 · Vite · Vue Router · Chart.js
**Database** SQLite (PostgreSQL-compatible via `DATABASE_URL`)

## Features

### Dashboard with monthly analytics

At-a-glance summary of the current month: total spent, transaction count,
daily average, active days. A doughnut chart breaks down spending by category,
and a line chart shows the daily trend. Use the month selector to navigate
historical periods.

![Dashboard](docs/screenshots/dashboard.png)

### Transaction management with filtering

Full CRUD with server-side filtering by date range, category, and
description. Search input is debounced to avoid hammering the API. A modal
form handles both create and edit flows with inline validation messages from
the backend.

![Transactions list](docs/screenshots/transactions.png)
![Transaction form](docs/screenshots/transaction-form.png)

### Category management

Create custom categories with colors used throughout the app for
visualization. Deleting a category cascades to its transactions via an
explicit database constraint.

![Categories](docs/screenshots/categories.png)

## Architecture

```
expense-tracker/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── __init__.py         # application factory
│   │   ├── extensions.py       # SQLAlchemy, CORS, Migrate instances
│   │   ├── config.py           # environment-based configuration
│   │   ├── models.py           # ORM models
│   │   ├── schemas.py          # Pydantic validation schemas
│   │   ├── errors.py           # centralized error handlers
│   │   └── api/
│   │       ├── categories.py   # /api/categories endpoints
│   │       ├── transactions.py # /api/transactions endpoints
│   │       └── stats.py        # /api/stats aggregation endpoints
│   ├── migrations/             # Alembic migration scripts
│   ├── seed.py                 # example data generator
│   └── run.py                  # entry point
│
├── frontend/                   # Vue 3 SPA
│   └── src/
│       ├── api/                # thin wrappers over fetch, one file per resource
│       ├── composables/        # reusable reactive logic (useApi, useDebouncedRef)
│       ├── components/         # reusable UI (BaseButton, BaseModal, charts...)
│       ├── views/              # one component per route
│       ├── utils/              # formatting helpers
│       └── router/             # route definitions
│
├── API.md                      # full REST API reference
└── README.md
```

### Design decisions worth mentioning

- **Application factory pattern** on the backend, with blueprints per resource.
  Makes the app testable and avoids circular imports.
- **Pydantic schemas** centralize input validation. Endpoints never validate
  manually — they parse a schema, and invalid input becomes a structured 400
  response.
- **`Numeric(12, 2)` for amounts**, never `Float`. Monetary precision is
  non-negotiable.
- **Aggregations happen in SQL**, not Python. Dashboard endpoints use
  `GROUP BY`, `SUM`, `COUNT` — no per-row iteration on the server.
- **Explicit foreign key enforcement in SQLite** via a connection-level
  `PRAGMA foreign_keys=ON` listener. Otherwise cascade deletes silently fail.
- **Frontend organized in layers**: an `api/` layer for HTTP, `composables/`
  for reusable reactive logic, `components/` for stateless UI, `views/` for
  route-level composition.
- **Error contract between backend and frontend** — backend returns
  `{ error, message, details? }` consistently, frontend maps validation
  details back to form field errors.

## Getting started

### Prerequisites

- Python 3.11 or newer
- Node.js 20 or newer
- Git

### Backend

```bash
git clone <repo-url>
cd expense-tracker
python -m venv venv
# Windows:     .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

cd backend
flask db upgrade            # create the database
python seed.py              # optional: load example data
flask run                   # starts on http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                 # starts on http://localhost:5173
```

Vite proxies `/api/*` requests to the Flask backend, so no CORS configuration
is needed during development.

## API reference

See [API.md](./API.md) for the full REST API specification — endpoints,
request/response schemas, query parameters, and error codes.

Quick overview:

| Method | Endpoint                    | Purpose                           |
|--------|-----------------------------|-----------------------------------|
| GET    | `/api/categories`           | List all categories               |
| POST   | `/api/categories`           | Create a category                 |
| PUT    | `/api/categories/<id>`      | Update a category (partial)       |
| DELETE | `/api/categories/<id>`      | Delete a category and its data    |
| GET    | `/api/transactions`         | List transactions with filtering  |
| POST   | `/api/transactions`         | Create a transaction              |
| PUT    | `/api/transactions/<id>`    | Update a transaction (partial)    |
| DELETE | `/api/transactions/<id>`    | Delete a transaction              |
| GET    | `/api/stats/summary`        | Monthly totals and counts         |
| GET    | `/api/stats/by-category`    | Spending breakdown by category    |
| GET    | `/api/stats/trend`          | Time-series data for charts       |

## Configuration

| Variable       | Default                              | Description                    |
|----------------|--------------------------------------|--------------------------------|
| `SECRET_KEY`   | `dev-key-change-me`                  | Flask signing key              |
| `DATABASE_URL` | `sqlite:///instance/expenses.db`     | SQLAlchemy connection string   |

To use PostgreSQL:

```bash
export DATABASE_URL="postgresql://user:password@localhost/expenses"
flask db upgrade
flask run
```

## License

Personal portfolio project — free to use as a reference.