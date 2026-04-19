# Expense Tracker

A personal expense tracking web application. Log transactions, browse their
history with filtering and sorting, manage expense categories, and analyze
spending habits through a dashboard with charts and summaries.

Single-user and local — no authentication, no cloud deployment. Intended to be
run on your own machine as a personal tool.

## Stack

- **Backend:** Python 3.14, Flask, Flask-SQLAlchemy, Flask-Migrate, Pydantic
- **Frontend:** Vue 3, Vite *(in progress)*
- **Database:** SQLite (default), any SQLAlchemy-supported backend via
  `DATABASE_URL`
- **Communication:** REST API, JSON payloads

## Project structure

```
expense-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # application factory
│   │   ├── extensions.py     # SQLAlchemy, Migrate, CORS instances
│   │   ├── config.py         # configuration
│   │   ├── models.py         # ORM models
│   │   ├── schemas.py        # Pydantic validation schemas
│   │   ├── errors.py         # centralized error handlers
│   │   └── api/
│   │       ├── categories.py   # /api/categories blueprint
│   │       ├── transactions.py # /api/transactions blueprint
│   │       ├── stats.py        # /api/stats blueprint
│   │       └── stats_helpers.py
│   ├── migrations/           # Alembic migration scripts
│   ├── instance/             # SQLite database (gitignored)
│   ├── run.py                # entrypoint
│   └── .flaskenv             # Flask environment variables
├── frontend/                 # Vue 3 application (in progress)
├── API.md                    # REST API reference
├── README.md
├── requirements.txt
└── .gitignore
```

## Running the backend

### Prerequisites

- Python 3.11 or newer
- Git

### Setup

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd expense-tracker
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```bash
   cd backend
   flask db upgrade
   ```

5. Start the development server:

   ```bash
   flask run
   ```

   The API is now available at `http://localhost:5000`. Try it:

   ```bash
   curl http://localhost:5000/
   # {"status": "ok", "service": "expense-tracker-api"}
   ```

### Configuration

Configuration is read from environment variables:

| Variable       | Default                              | Description                   |
|----------------|--------------------------------------|-------------------------------|
| `SECRET_KEY`   | `dev-key-change-me`                  | Flask session/signing key     |
| `DATABASE_URL` | `sqlite:///instance/expenses.db`     | SQLAlchemy database URI       |

To use PostgreSQL instead of SQLite:

```bash
# Example
export DATABASE_URL="postgresql://user:password@localhost/expenses"
flask db upgrade
flask run
```

## API reference

See [API.md](./API.md) for the full REST API specification, including request
and response schemas, query parameters, and error codes.

Quick overview:

- `GET/POST/PUT/DELETE /api/categories` — manage expense categories
- `GET/POST/PUT/DELETE /api/transactions` — manage transactions, with
  filtering by date range, category, and description
- `GET /api/stats/summary` — monthly totals, count, average
- `GET /api/stats/by-category` — spending breakdown by category
- `GET /api/stats/trend` — time-series spending data

## Development notes

- Database migrations are managed by Flask-Migrate (Alembic). After changing
  a model, run `flask db migrate -m "describe change"` then
  `flask db upgrade`.
- All input validation is handled by Pydantic schemas in `app/schemas.py`.
  Endpoints should not contain manual validation logic.
- Error responses follow a consistent JSON format (see API.md). Custom error
  handlers are registered in `app/errors.py`.
- SQLite foreign key enforcement is explicitly enabled via a connection-level
  `PRAGMA foreign_keys=ON` listener in `app/extensions.py`.
- Monetary amounts are stored as `Numeric(12, 2)` and serialized as strings
  to prevent floating-point precision loss.

## Status

- [x] Backend: categories CRUD
- [x] Backend: transactions CRUD with filtering
- [x] Backend: statistics endpoints
- [ ] Frontend: Vue 3 application
- [ ] Frontend: dashboard with charts
- [ ] End-to-end testing

## License

Personal portfolio project.