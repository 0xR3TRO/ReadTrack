# ReadTrack — API Reference

All API endpoints are prefixed with `/api`. Responses follow a consistent JSON envelope:

```json
{
  "success": true,
  "message": "...",
  "data": { ... }
}
```

Error responses:

```json
{
    "success": false,
    "message": "Error description"
}
```

## Authentication

All endpoints except `/api/auth/register` and `/api/auth/login` require a valid JWT access token in the `Authorization: Bearer <token>` header.

### POST /api/auth/register

Register a new user.

**Request body:**

```json
{
    "username": "string (3-80 chars, alphanumeric + _-)",
    "email": "string (valid email)",
    "password": "string (min 8 chars)"
}
```

**Response (201):**

```json
{
    "success": true,
    "message": "Registration successful",
    "data": {
        "user": { "id": 1, "username": "...", "email": "..." },
        "access_token": "...",
        "refresh_token": "..."
    }
}
```

### POST /api/auth/login

**Request body:**

```json
{ "username": "string", "password": "string" }
```

**Response (200):** Same structure as register.

### POST /api/auth/refresh

Requires `refresh_token` in Authorization header.

**Response (200):**

```json
{ "success": true, "data": { "access_token": "..." } }
```

### GET /api/auth/me

Get current user info.

**Response (200):**

```json
{ "success": true, "data": { "id": 1, "username": "...", "email": "..." } }
```

---

## Books

### GET /api/books

List all books for the current user.

**Query params:** `status` (unread|reading|completed|on_hold), `search` (title search).

**Response (200):**

```json
{ "success": true, "data": [{ "id": 1, "title": "...", "status": "reading", ... }] }
```

### POST /api/books

Create a book.

**Request body:**

```json
{
    "title": "string (required)",
    "isbn": "string",
    "genre": "string",
    "publisher": "string",
    "published_date": "string",
    "description": "string",
    "total_pages": 0,
    "total_chapters": 0,
    "status": "unread",
    "rating": null,
    "author_ids": [1, 2]
}
```

**Response (201):** Created book object.

### GET /api/books/:id

Get book details (includes authors, notes, files).

### PUT /api/books/:id

Update book fields.

### DELETE /api/books/:id

Delete a book (204 No Content).

### PATCH /api/books/:id/progress

Update reading progress.

**Request body:**

```json
{
    "current_page": 150,
    "current_chapter": 5,
    "status": "reading"
}
```

---

## Authors

### GET /api/authors

List all authors. **Query params:** `search`.

### POST /api/authors

**Request body:**

```json
{
    "name": "string (required)",
    "biography": "string",
    "birth_date": "string",
    "website": "string"
}
```

### GET /api/authors/:id

Get author details (includes books).

### PUT /api/authors/:id

Update author.

### DELETE /api/authors/:id

Delete author (204).

---

## Notes (nested under books)

### GET /api/books/:book_id/notes

List notes for a book.

### POST /api/books/:book_id/notes

**Request body:**

```json
{ "content": "string (required)", "page_number": null, "chapter": null }
```

### PUT /api/books/:book_id/notes/:note_id

Update a note.

### DELETE /api/books/:book_id/notes/:note_id

Delete a note (204).

---

## Files (nested under books)

### GET /api/books/:book_id/files

List files for a book.

### POST /api/books/:book_id/files

Upload a file (multipart/form-data). Field name: `file`.

Allowed extensions: pdf, txt, doc, docx, epub, mobi, png, jpg, jpeg.

Max size: 16 MB.

### GET /api/books/:book_id/files/:file_id

Download a file.

### DELETE /api/books/:book_id/files/:file_id

Delete a file (204).
