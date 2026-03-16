# ReadTrack — Usage Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ReadTrack
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r server/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your own SECRET_KEY and JWT_SECRET_KEY

# Run the server
cd server
python app.py
```

The backend runs at `http://localhost:5000`.

### 3. Frontend Setup

```bash
cd client
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API calls to the backend.

## Using the Application

### Register

1. Open `http://localhost:5173/register`.
2. Enter a username (3+ characters), email, and password (8+ characters).
3. You will be redirected to the dashboard.

### Add a Book

1. Click **Add Book** on the dashboard or books page.
2. Fill in the title (required) and optional fields (genre, publisher, ISBN, etc.).
3. Set total pages/chapters for progress tracking.
4. Select authors if any have been added.
5. Click **Add Book**.

### Track Reading Progress

1. Navigate to a book's detail page.
2. Update the current page, current chapter, and status.
3. Click **Update Progress** — the progress bar updates immediately.

### Add Notes

1. On the book detail page, scroll to the **Notes** section.
2. Type your note content and optionally enter a page number.
3. Click **Add Note**.

### Upload Files

1. On the book detail page, scroll to the **Files** section.
2. Click **Choose File** and select a file (PDF, TXT, DOC, EPUB, PNG, JPG — max 16 MB).
3. The file appears in the list with download and delete options.

### Manage Authors

1. Go to the **Authors** page.
2. Click **Add Author** and fill in name, biography, birth date, and website.
3. Authors can be linked to books when creating or editing a book.
