# ReadTrack — Testing

## Test Stack

- **pytest** — Test runner
- **pytest-flask** — Flask test client integration
- **SQLite in-memory** — Tests use `TestConfig` with `sqlite:///:memory:` for isolation

## Running Tests

```bash
cd server
source ../venv/bin/activate
python -m pytest tests/ -v
```

## Test Structure

```
server/tests/
├── conftest.py        # Shared fixtures (app, db, client, auth_headers)
├── test_auth.py       # Authentication tests (11 tests)
├── test_books.py      # Book CRUD + progress tests (11 tests)
├── test_authors.py    # Author CRUD tests (8 tests)
├── test_notes.py      # Note CRUD tests (6 tests)
└── test_files.py      # File upload/download/delete tests (7 tests)
```

**Total: 43 tests**

## Test Categories

### Unit/Integration Tests

| Module  | Tests | Coverage                                                                                                                                                 |
| ------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Auth    | 11    | Register (success, duplicate, invalid email, short password, no body), Login (success, wrong password, nonexistent), Refresh, Me (success, unauthorized) |
| Books   | 11    | Create (success, missing title, unauthorized), List (empty, populated, filter by status), Get (success, not found), Update, Delete, Progress update      |
| Authors | 8     | Create (success, missing name, unauthorized), List, Get (success, not found), Update, Delete                                                             |
| Notes   | 6     | Create (success, missing content, book not found), List, Update, Delete                                                                                  |
| Files   | 7     | Upload (success, invalid extension, no file, book not found), List, Download, Delete                                                                     |

### Security Tests

- JWT required endpoints return 401 without token
- Users cannot access other users' data (books/authors are per-user)
- File upload rejects disallowed extensions
- Passwords are hashed (never stored in plain text)

## Fixtures

- `app` — Flask application with TestConfig
- `db` — Fresh database per test (create_all/drop_all)
- `client` — Flask test client
- `auth_headers` — Pre-authenticated headers (registers a test user)
- `refresh_headers` — Headers with refresh token

## Adding New Tests

1. Create a new test file in `server/tests/`.
2. Use the shared fixtures from `conftest.py`.
3. Follow the existing pattern: create test data, call endpoint, assert response.
