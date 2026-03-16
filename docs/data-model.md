# ReadTrack — Data Model

## Entity-Relationship Diagram

```
┌──────────┐       ┌──────────────┐       ┌──────────┐
│  Users   │──1:N──│    Books     │──M:N──│ Authors  │
└──────────┘       └──────────────┘       └──────────┘
     │                  │     │
     │                  1:N   1:N
     │                  │     │
     │              ┌───┘     └───┐
     │              ▼             ▼
     │         ┌─────────┐  ┌─────────┐
     └──1:N───│  Notes   │  │  Files  │
              └─────────┘  └─────────┘
```

## Models

### User

| Column        | Type        | Constraints                 |
| ------------- | ----------- | --------------------------- |
| id            | Integer     | Primary key, auto-increment |
| username      | String(80)  | Unique, not null, indexed   |
| email         | String(120) | Unique, not null, indexed   |
| password_hash | String(256) | Not null                    |
| created_at    | DateTime    | Default: now (UTC)          |
| updated_at    | DateTime    | Default: now, auto-update   |

**Relationships:** Has many Books, Notes, Authors, Files (cascade delete).

### Book

| Column          | Type        | Constraints               |
| --------------- | ----------- | ------------------------- |
| id              | Integer     | Primary key               |
| title           | String(200) | Not null                  |
| isbn            | String(13)  | Nullable                  |
| genre           | String(100) | Nullable                  |
| publisher       | String(200) | Nullable                  |
| published_date  | String(20)  | Nullable                  |
| description     | Text        | Nullable                  |
| cover_image     | String(500) | Nullable                  |
| total_pages     | Integer     | Default: 0                |
| current_page    | Integer     | Default: 0                |
| total_chapters  | Integer     | Default: 0                |
| current_chapter | Integer     | Default: 0                |
| status          | String(20)  | Default: "unread"         |
| rating          | Integer     | Nullable (1-5)            |
| user_id         | Integer     | Foreign key → users.id    |
| created_at      | DateTime    | Default: now (UTC)        |
| updated_at      | DateTime    | Default: now, auto-update |

**Relationships:** Many-to-many with Authors (via `book_authors`), has many Notes and Files.

**Computed:** `progress_percentage()` = `(current_page / total_pages) * 100`

### Author

| Column     | Type        | Constraints               |
| ---------- | ----------- | ------------------------- |
| id         | Integer     | Primary key               |
| name       | String(200) | Not null                  |
| biography  | Text        | Nullable                  |
| birth_date | String(20)  | Nullable                  |
| website    | String(500) | Nullable                  |
| user_id    | Integer     | Foreign key → users.id    |
| created_at | DateTime    | Default: now (UTC)        |
| updated_at | DateTime    | Default: now, auto-update |

**Relationships:** Many-to-many with Books.

### Note

| Column      | Type     | Constraints               |
| ----------- | -------- | ------------------------- |
| id          | Integer  | Primary key               |
| content     | Text     | Not null                  |
| page_number | Integer  | Nullable                  |
| chapter     | Integer  | Nullable                  |
| book_id     | Integer  | Foreign key → books.id    |
| user_id     | Integer  | Foreign key → users.id    |
| created_at  | DateTime | Default: now (UTC)        |
| updated_at  | DateTime | Default: now, auto-update |

### File

| Column            | Type        | Constraints             |
| ----------------- | ----------- | ----------------------- |
| id                | Integer     | Primary key             |
| filename          | String(500) | Not null (UUID on disk) |
| original_filename | String(500) | Not null (user-facing)  |
| file_type         | String(100) | Nullable                |
| file_size         | Integer     | Nullable (bytes)        |
| book_id           | Integer     | Foreign key → books.id  |
| user_id           | Integer     | Foreign key → users.id  |
| created_at        | DateTime    | Default: now (UTC)      |

### book_authors (Association Table)

| Column    | Type    | Constraints                  |
| --------- | ------- | ---------------------------- |
| book_id   | Integer | Primary key, FK → books.id   |
| author_id | Integer | Primary key, FK → authors.id |
