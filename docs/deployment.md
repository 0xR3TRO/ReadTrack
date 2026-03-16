# ReadTrack — Deployment Guide

## Development Environment

### Backend

```bash
cd server
source ../venv/bin/activate
python app.py
# Runs on http://localhost:5000 with debug mode
```

### Frontend

```bash
cd client
npm run dev
# Runs on http://localhost:5173 with HMR
```

## Production Build

### Frontend

```bash
cd client
npm run build
# Outputs to client/dist/
```

The `dist/` folder contains static files ready for deployment.

### Backend

1. Set environment variables (do not use defaults):

```bash
export SECRET_KEY="your-random-secret-key"
export JWT_SECRET_KEY="your-different-random-jwt-key"
export FLASK_ENV=production
```

2. Use a production WSGI server:

```bash
pip install gunicorn
cd server
gunicorn "app:create_app()" -b 0.0.0.0:5000 -w 4
```

## Deployment Options

### Backend (Python hosting)

- **Railway / Render** — Push the `server/` directory, set Python buildpack, set env vars.
- **VPS (Ubuntu)** — Install Python, clone repo, set up systemd service for gunicorn, use nginx as reverse proxy.
- **Docker** — Create a Dockerfile based on `python:3.12-slim`, install requirements, run gunicorn.

### Frontend (Static hosting)

- **Netlify / Vercel** — Connect repo, set build command to `cd client && npm run build`, publish directory to `client/dist`.
- **Nginx** — Serve `client/dist/` as static files, configure SPA fallback to `index.html`.

### Environment Variables

| Variable           | Description              | Required |
| ------------------ | ------------------------ | -------- |
| SECRET_KEY         | Flask secret key         | Yes      |
| JWT_SECRET_KEY     | JWT signing key          | Yes      |
| DATABASE_URL       | SQLite URI (or other DB) | No       |
| UPLOAD_FOLDER      | File upload directory    | No       |
| MAX_CONTENT_LENGTH | Max upload size in bytes | No       |

## CORS Configuration

In production, update the CORS configuration in `app.py` to restrict allowed origins to your frontend domain instead of `"*"`.
