# Expense Tracker API

Base URL: `http://localhost:5000`

## Categories

### `GET /api/categories`
Returns a list of all categories, sorted alphabetically.

**Response 200:**
```json
[
  {“id”: 1, “name”: “Food”, “color”: “#E24B4A”, ‘created_at’: “2026-04-19T10:30:00”},
  {“id”: 2, “name”: “Transport”, “color”: “#378ADD”, ‘created_at’: “2026-04-19T10:31:00”}
]
```

### `GET /api/categories/<id>`
Returns a single category.

**Response 200:** category object.
**Response 404:** category does not exist.

### `POST /api/categories`
Creates a new category.

**Request body:**
```json
{“name”: “Food”, ‘color’: “#E24B4A”}
```

- `name` — required, 1–50 characters (after stripping).
- `color` — optional (default `#888888`), format `#RRGGBB`.

**Response 201:** category created.
**Response 400:** validation error.
**Response 409:** name already exists.

### `PUT /api/categories/<id>`
Updates a category. Both fields are optional — only the ones sent are updated.

**Request body (example — changing the color only):**
```json
{“color”: “#F0997B”}
```

**Response 200:** Category updated.
**Response 400:** Validation error.
**Response 404:** Category does not exist.

### `DELETE /api/categories/<id>`
Deletes a category.

**Response 204:** success, empty body.
**Response 404:** category does not exist.

Translated with DeepL.com (free version)