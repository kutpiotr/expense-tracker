# Expense Tracker — REST API reference

Base URL: `http://localhost:5000`

All request and response bodies use JSON. Monetary amounts are represented as
strings (e.g. `"12.50"`) to preserve decimal precision. Dates use ISO 8601
format (`YYYY-MM-DD`). Timestamps use ISO 8601 with second precision
(`YYYY-MM-DDTHH:MM:SS`).

## Error format

All error responses use a consistent JSON shape:

```json
{
  "error": "<error_code>",
  "message": "<human-readable message>"
}
```

Validation errors additionally include a `details` array with per-field messages:

```json
{
  "error": "validation_error",
  "details": [
    {"field": "name", "message": "String should have at least 1 character"},
    {"field": "color", "message": "Value error, color must be a hex code in format #RRGGBB"}
  ]
}
```

| HTTP status | `error` code          | Meaning                                      |
|-------------|-----------------------|----------------------------------------------|
| 400         | `validation_error`    | Request body failed schema validation        |
| 400         | `bad_request`         | Malformed query parameter or request         |
| 400         | `invalid_reference`   | Referenced resource (e.g. category) missing  |
| 404         | `not_found`           | Resource with given id does not exist        |
| 409         | `integrity_error`     | Database constraint violated (e.g. duplicate)|

---

## Health check

### `GET /`

Returns service metadata. Useful for smoke-testing that the server is running.

**Response 200**

```json
{"status": "ok", "service": "expense-tracker-api"}
```

---

## Categories

A category represents a logical group of expenses (e.g. "Food", "Transport").
Each category has a unique name and a hex color used by the frontend for
visualization.

### `GET /api/categories`

Returns all categories, sorted alphabetically by name.

**Response 200**

```json
[
  {
    "id": 1,
    "name": "Food",
    "color": "#E24B4A",
    "created_at": "2026-04-19T10:30:00"
  },
  {
    "id": 2,
    "name": "Transport",
    "color": "#378ADD",
    "created_at": "2026-04-19T10:31:00"
  }
]
```

### `GET /api/categories/<id>`

Returns a single category by id.

**Response 200** — category object (same shape as list elements).
**Response 404** — category not found.

### `POST /api/categories`

Creates a new category.

**Request body**

```json
{
  "name": "Food",
  "color": "#E24B4A"
}
```

| Field   | Type   | Required | Constraints                                |
|---------|--------|----------|--------------------------------------------|
| `name`  | string | yes      | 1–50 characters after trim, must be unique |
| `color` | string | no       | Hex format `#RRGGBB`, defaults to `#888888`|

**Response 201** — created category.
**Response 400** — validation error.
**Response 409** — name already exists.

### `PUT /api/categories/<id>`

Partially updates a category. Any field omitted from the request body is left
unchanged.

**Request body (partial update example)**

```json
{"color": "#F0997B"}
```

**Response 200** — updated category.
**Response 400** — validation error.
**Response 404** — category not found.
**Response 409** — name collision with another category.

### `DELETE /api/categories/<id>`

Deletes a category and **all its transactions** (cascade).

**Response 204** — no content.
**Response 404** — category not found.

---

## Transactions

A transaction represents a single expense entry, always associated with a
category.

### `GET /api/transactions`

Returns transactions ordered by date descending, then by creation time
descending.

**Query parameters (all optional)**

| Parameter     | Type   | Description                                       |
|---------------|--------|---------------------------------------------------|
| `from`        | date   | Include transactions on or after this date        |
| `to`          | date   | Include transactions on or before this date       |
| `category_id` | int    | Filter by category id                             |
| `q`           | string | Case-insensitive substring match on `description` |

Parameters combine with AND semantics.

**Example**

```
GET /api/transactions?from=2026-04-01&to=2026-04-30&category_id=1&q=coffee
```

**Response 200**

```json
[
  {
    "id": 42,
    "amount": "12.50",
    "transaction_date": "2026-04-15",
    "description": "Groceries",
    "category_id": 1,
    "category": {
      "id": 1,
      "name": "Food",
      "color": "#E24B4A"
    },
    "created_at": "2026-04-19T10:32:00"
  }
]
```

**Response 400** — invalid date format in query parameter.

### `GET /api/transactions/<id>`

Returns a single transaction by id.

**Response 200** — transaction object.
**Response 404** — transaction not found.

### `POST /api/transactions`

Creates a new transaction.

**Request body**

```json
{
  "amount": "12.50",
  "transaction_date": "2026-04-15",
  "description": "Groceries",
  "category_id": 1
}
```

| Field              | Type    | Required | Constraints                           |
|--------------------|---------|----------|---------------------------------------|
| `amount`           | number  | yes      | Greater than 0, up to 2 decimal places|
| `transaction_date` | date    | yes      | ISO format `YYYY-MM-DD`               |
| `description`      | string  | no       | Up to 255 characters, defaults to ""  |
| `category_id`      | int     | yes      | Must reference an existing category   |

**Response 201** — created transaction.
**Response 400** — validation error or nonexistent category.

### `PUT /api/transactions/<id>`

Partially updates a transaction. Any field omitted from the request body is
left unchanged.

**Response 200** — updated transaction.
**Response 400** — validation error or nonexistent category.
**Response 404** — transaction not found.

### `DELETE /api/transactions/<id>`

Deletes a transaction.

**Response 204** — no content.
**Response 404** — transaction not found.

---

## Statistics

Aggregation endpoints powering the dashboard. All computation happens in SQL
(GROUP BY, SUM, COUNT, AVG) — no per-row iteration on the server.

### `GET /api/stats/summary`

Summary of a single calendar month.

**Query parameters**

| Parameter | Type | Required | Description                           |
|-----------|------|----------|---------------------------------------|
| `year`    | int  | no       | 2000–2100; defaults to current month  |
| `month`   | int  | no       | 1–12; defaults to current month       |

If no parameters are provided, the current month is used. If provided, both
must be given together.

**Response 200**

```json
{
  "period": {
    "from": "2026-04-01",
    "to": "2026-04-30"
  },
  "total": "151.40",
  "count": 5,
  "average": "30.28",
  "days_with_expenses": 5
}
```

### `GET /api/stats/by-category`

Sum and count of transactions grouped by category, with each category's share
of the total as a percentage. Ordered by total descending.

**Query parameters**

| Parameter   | Type | Description                                   |
|-------------|------|-----------------------------------------------|
| `date_from` | date | Include transactions on or after this date    |
| `date_to`   | date | Include transactions on or before this date   |

If no parameters are provided, the current month is used.

**Response 200**

```json
[
  {
    "category_id": 1,
    "category_name": "Food",
    "category_color": "#E24B4A",
    "total": "21.40",
    "count": 2,
    "percentage": 14.13
  },
  {
    "category_id": 2,
    "category_name": "Transport",
    "category_color": "#378ADD",
    "total": "70.00",
    "count": 2,
    "percentage": 46.24
  },
  {
    "category_id": 3,
    "category_name": "Entertainment",
    "category_color": "#AFA9EC",
    "total": "60.00",
    "count": 1,
    "percentage": 39.63
  }
]
```

Note: categories with no transactions in the given period are currently
excluded from the result.

### `GET /api/stats/trend`

Sum and count of transactions grouped by time period. Used for rendering
time-series charts.

**Query parameters**

| Parameter     | Type                 | Description                                      |
|---------------|----------------------|--------------------------------------------------|
| `date_from`   | date                 | Start of range                                   |
| `date_to`     | date                 | End of range                                     |
| `granularity` | `"day"` \| `"month"` | Time bucket size; defaults to `"day"`            |

If no parameters are provided, the current month is used with daily granularity.

**Response 200**

```json
{
  "granularity": "day",
  "period": {
    "from": "2026-04-01",
    "to": "2026-04-30"
  },
  "data": [
    {"period": "2026-04-01", "total": "12.50", "count": 1},
    {"period": "2026-04-03", "total": "8.90",  "count": 1},
    {"period": "2026-04-05", "total": "45.00", "count": 1},
    {"period": "2026-04-10", "total": "60.00", "count": 1},
    {"period": "2026-04-15", "total": "25.00", "count": 1}
  ]
}
```

For `granularity=month`, the `period` field on each data point is in `YYYY-MM`
format.

---

## Notes

- The API is single-user and does not require authentication.
- The database is SQLite by default. Setting the `DATABASE_URL` environment
  variable switches to any SQLAlchemy-supported backend (e.g. PostgreSQL).
- CORS is enabled for `http://localhost:5173` (the Vite development server).