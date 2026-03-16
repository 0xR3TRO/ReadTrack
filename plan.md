# ReadTrack Implementation Plan

## Current State

- `server/config.py`, `database.py`, `requirements.txt` exist with Flask/JWT/SQLAlchemy config
- Empty server subdirectories (models, routes, controllers, services, utils, tests)
- No `app.py`, no `client/`, no `docs/`, no `README.md`

## Phase 1: Backend (server/)

### Step 1.1 — Package init files

Create `__init__.py` in all server packages.

### Step 1.2 — Models (5 files)

- `models/user.py` — User (username, email, password_hash, timestamps, relationships)
- `models/book.py` — Book (title, isbn, publisher, genre, total_pages, current_page, total_chapters, current_chapter, status, rating) + `book_authors` M2M table
- `models/author.py` — Author (name, biography, birth_date, website, user_id)
- `models/note.py` — Note (content, page_number, chapter, book_id, user_id)
- `models/file.py` — File (filename, original_filename, file_type, file_size, book_id, user_id)

### Step 1.3 — Utilities

- `utils/validators.py` — email, password, username, rating, status validation
- `utils/responses.py` — consistent JSON response helpers
- `utils/file_handler.py` — file upload/delete with secure filenames

### Step 1.4 — Services (business logic)

- `services/auth_service.py` — register, login, password hashing
- `services/book_service.py` — CRUD, progress update, search
- `services/author_service.py` — CRUD
- `services/note_service.py` — CRUD per book
- `services/file_service.py` — upload, delete, list per book

### Step 1.5 — Controllers (request handling)

- `controllers/auth_controller.py` — register, login, refresh, me, logout
- `controllers/book_controller.py` — CRUD endpoints + progress
- `controllers/author_controller.py` — CRUD endpoints
- `controllers/note_controller.py` — CRUD per book
- `controllers/file_controller.py` — upload, download, delete per book

### Step 1.6 — Routes (Blueprint registration)

- `routes/auth_routes.py` — /api/auth/\*
- `routes/book_routes.py` — /api/books/\*
- `routes/author_routes.py` — /api/authors/\*
- `routes/note_routes.py` — /api/books/<id>/notes/\*
- `routes/file_routes.py` — /api/books/<id>/files/\*

### Step 1.7 — Application factory

- `app.py` — create_app() with Flask factory pattern, register blueprints, CORS, JWT, db init

### Step 1.8 — Update config.py

- Wrap JWT expiry values in `timedelta`

## Phase 2: Frontend (client/) — React + Vite

### Step 2.1 — Scaffold with Vite

Create React project at `client/` using Vite.

### Step 2.2 — Services (API layer)

- `services/api.js` — Axios instance with JWT interceptors
- `services/authService.js` — login, register, refresh, logout
- `services/bookService.js` — CRUD + progress
- `services/authorService.js` — CRUD
- `services/noteService.js` — CRUD
- `services/fileService.js` — upload, download, delete

### Step 2.3 — Context & Hooks

- `context/AuthContext.jsx` — auth state, login/logout, token persistence
- `hooks/useBooks.js`, `hooks/useAuthors.js` — data fetching hooks

### Step 2.4 — Components

- `components/Navbar.jsx` — navigation bar
- `components/ProgressBar.jsx` — reading progress visualization
- `components/BookCard.jsx` — book card for list views
- `components/NoteList.jsx` — notes display & add
- `components/FileUpload.jsx` — file upload widget
- `components/ProtectedRoute.jsx` — auth guard

### Step 2.5 — Pages

- `pages/Home.jsx` — dashboard with progress, recent books
- `pages/Login.jsx` — login form
- `pages/Register.jsx` — registration form
- `pages/Books.jsx` — book list
- `pages/BookDetail.jsx` — single book with progress, notes, files
- `pages/AddBook.jsx` — add/edit book form
- `pages/Authors.jsx` — author list
- `pages/AuthorDetail.jsx` — single author with publications
- `pages/AddAuthor.jsx` — add/edit author form

### Step 2.6 — App.jsx & Styles

- `App.jsx` — React Router setup
- `styles/` — CSS for all components, responsive design

## Phase 3: Tests (server/tests/)

- `conftest.py` — Flask test client, test DB fixtures
- `test_auth.py` — register, login, refresh, protected routes
- `test_books.py` — CRUD, progress, search
- `test_authors.py` — CRUD
- `test_notes.py` — CRUD per book
- `test_files.py` — upload, download, delete

## Phase 4: Documentation (docs/)

- `overview.md` — project description & features
- `architecture.md` — system architecture & MVC pattern
- `api.md` — full API reference
- `data-model.md` — ER diagram & model descriptions
- `usage-guide.md` — setup & usage instructions
- `testing.md` — test plan & procedures
- `deployment.md` — deployment guide
- `maintenance.md` — maintenance procedures

## Phase 5: README.md

- Full project README with description, features, tech stack, setup, API overview, architecture, future improvements, license
