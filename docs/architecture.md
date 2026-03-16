# ReadTrack — System Architecture

## Overview

ReadTrack follows an **MVC-inspired architecture** with a clear separation between the React frontend (View), Flask controllers (Controller), and the service/model layers (Model).

## High-Level Diagram

```
┌─────────────────────────────┐
│       React Frontend        │
│  (Vite + React Router)      │
│  Pages → Components         │
│  Context → Services (Axios) │
└────────────┬────────────────┘
             │ HTTP (JSON)
             ▼
┌─────────────────────────────┐
│        Flask Backend        │
│                             │
│  Routes → Controllers       │
│  Controllers → Services     │
│  Services → Models (ORM)    │
│  Models → SQLite Database   │
└─────────────────────────────┘
```

## Backend Architecture

```
server/
├── app.py              # Application factory (create_app)
├── config.py           # Configuration classes
├── database.py         # SQLAlchemy instance
├── models/             # SQLAlchemy ORM models
│   ├── user.py         # User model
│   ├── book.py         # Book model + book_authors M2M table
│   ├── author.py       # Author model
│   ├── note.py         # Note model
│   └── file.py         # File model
├── routes/             # Flask Blueprints (URL → controller mapping)
├── controllers/        # Request handling (parse input, call service, return response)
├── services/           # Business logic (validation, DB operations)
├── utils/              # Shared utilities (validators, response helpers, file handler)
└── tests/              # pytest test suite
```

### Layer Responsibilities

- **Routes**: Define URL patterns and HTTP methods, map to controller functions via Flask Blueprints.
- **Controllers**: Parse request data, call service functions, format HTTP responses.
- **Services**: Contain all business logic — validation, database queries, file operations.
- **Models**: Define database schema using SQLAlchemy ORM, provide `to_dict()` serialization.
- **Utils**: Shared helpers — input validators, consistent JSON responses, file upload handling.

## Frontend Architecture

```
client/src/
├── services/           # Axios API layer (one file per resource)
├── context/            # React Context (AuthContext for auth state)
├── hooks/              # Custom hooks (useBooks, useAuthors)
├── components/         # Reusable UI components
├── pages/              # Page-level components (routed via React Router)
├── styles/             # CSS modules per component/page
└── App.jsx             # Root component with routing
```

## Authentication Flow

1. User registers or logs in via `/api/auth/register` or `/api/auth/login`.
2. Server returns `access_token` (1 hour) and `refresh_token` (30 days).
3. Client stores tokens in `localStorage` and attaches `access_token` to every API request via Axios interceptor.
4. When `access_token` expires (401 response), the interceptor automatically calls `/api/auth/refresh` with the `refresh_token`.
5. If refresh fails, the user is redirected to the login page.

## Database

SQLite is used as the database engine. SQLAlchemy ORM handles all database operations. The database file is created automatically on first run via `db.create_all()` in the application factory.
