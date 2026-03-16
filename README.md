# ReadTrack

A comprehensive book management system that enables users to track their reading progress, store notes and files, and manage detailed information about books and authors.

## Features

- **Reading Progress** — Track pages and chapters read with visual progress bars
- **Notes** — Add notes tied to specific pages in a book
- **File Storage** — Upload and manage files (PDF, images, documents) per book
- **Book Management** — Full CRUD with title, genre, publisher, ISBN, rating, status
- **Author Management** — Author profiles with biographies and linked publications
- **Authentication** — Secure JWT-based registration and login with token refresh
- **Responsive UI** — Modern React interface for desktop and mobile

## Tech Stack

| Layer    | Technology                                    |
| -------- | --------------------------------------------- |
| Frontend | React 19, Vite, React Router, Axios           |
| Backend  | Flask 3, Flask-SQLAlchemy, Flask-JWT-Extended |
| Database | SQLite                                        |
| Testing  | pytest (43 tests)                             |

## Project Structure

```
ReadTrack/
├── client/                 # React frontend (Vite)
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components (routed)
│   │   ├── context/        # React Context (auth)
│   │   ├── services/       # API service layer (Axios)
│   │   ├── hooks/          # Custom React hooks
│   │   └── styles/         # CSS files
│   └── package.json
├── server/                 # Flask backend
│   ├── app.py              # Application factory
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # Flask Blueprints
│   ├── controllers/        # Request handlers
│   ├── services/           # Business logic
│   ├── utils/              # Validators, helpers
│   ├── tests/              # pytest test suite
│   └── requirements.txt
├── docs/                   # Project documentation
├── .env.example
└── LICENSE
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt

cp .env.example .env
# Edit .env with your own secret keys

cd server
python app.py
```

Server runs at `http://localhost:5000`.

### Frontend

```bash
cd client
npm install
npm run dev
```

App runs at `http://localhost:5173`.

### Run Tests

```bash
cd server
python -m pytest tests/ -v
```

## API Overview

| Method | Endpoint                  | Description             |
| ------ | ------------------------- | ----------------------- |
| POST   | /api/auth/register        | Register a new user     |
| POST   | /api/auth/login           | Login                   |
| POST   | /api/auth/refresh         | Refresh access token    |
| GET    | /api/auth/me              | Get current user        |
| GET    | /api/books                | List books              |
| POST   | /api/books                | Create a book           |
| GET    | /api/books/:id            | Get book details        |
| PUT    | /api/books/:id            | Update a book           |
| DELETE | /api/books/:id            | Delete a book           |
| PATCH  | /api/books/:id/progress   | Update reading progress |
| GET    | /api/authors              | List authors            |
| POST   | /api/authors              | Create an author        |
| GET    | /api/authors/:id          | Get author details      |
| PUT    | /api/authors/:id          | Update an author        |
| DELETE | /api/authors/:id          | Delete an author        |
| GET    | /api/books/:id/notes      | List notes for a book   |
| POST   | /api/books/:id/notes      | Add a note              |
| PUT    | /api/books/:id/notes/:nid | Update a note           |
| DELETE | /api/books/:id/notes/:nid | Delete a note           |
| GET    | /api/books/:id/files      | List files for a book   |
| POST   | /api/books/:id/files      | Upload a file           |
| GET    | /api/books/:id/files/:fid | Download a file         |
| DELETE | /api/books/:id/files/:fid | Delete a file           |

See [docs/api.md](docs/api.md) for full API documentation.

## Documentation

- [Overview](docs/overview.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Data Model](docs/data-model.md)
- [Usage Guide](docs/usage-guide.md)
- [Testing](docs/testing.md)
- [Deployment](docs/deployment.md)
- [Maintenance](docs/maintenance.md)

## Future Improvements

- Database migrations with Flask-Migrate
- Pagination for list endpoints
- Full-text search
- Book cover image support
- Reading recommendations
- Data export (CSV, JSON)

## License

MIT License. See [LICENSE](LICENSE) for details.
