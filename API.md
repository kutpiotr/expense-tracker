# Expense Tracker API

Base URL: `http://localhost:5000`

## Categories

### `GET /api/categories`
Zwraca listę wszystkich kategorii, posortowanych alfabetycznie.

**Response 200:**
```json
[
  {"id": 1, "name": "Jedzenie", "color": "#E24B4A", "created_at": "2026-04-19T10:30:00"},
  {"id": 2, "name": "Transport", "color": "#378ADD", "created_at": "2026-04-19T10:31:00"}
]
```

### `GET /api/categories/<id>`
Zwraca pojedynczą kategorię.

**Response 200:** obiekt kategorii.
**Response 404:** kategoria nie istnieje.

### `POST /api/categories`
Tworzy nową kategorię.

**Request body:**
```json
{"name": "Jedzenie", "color": "#E24B4A"}
```

- `name` — wymagane, 1-50 znaków (po strip).
- `color` — opcjonalne (domyślnie `#888888`), format `#RRGGBB`.

**Response 201:** utworzona kategoria.
**Response 400:** błąd walidacji.
**Response 409:** nazwa już istnieje.

### `PUT /api/categories/<id>`
Aktualizuje kategorię. Oba pola opcjonalne — aktualizowane są tylko przesłane.

**Request body (przykład — sama zmiana koloru):**
```json
{"color": "#F0997B"}
```

**Response 200:** zaktualizowana kategoria.
**Response 400:** błąd walidacji.
**Response 404:** kategoria nie istnieje.

### `DELETE /api/categories/<id>`
Usuwa kategorię.

**Response 204:** sukces, pusty body.
**Response 404:** kategoria nie istnieje.