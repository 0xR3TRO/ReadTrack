from datetime import datetime, timezone

from database import db

book_authors = db.Table(
    "book_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id"), primary_key=True),
)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    isbn = db.Column(db.String(13), nullable=True)
    publisher = db.Column(db.String(200), nullable=True)
    published_date = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(500), nullable=True)

    total_pages = db.Column(db.Integer, default=0)
    current_page = db.Column(db.Integer, default=0)
    total_chapters = db.Column(db.Integer, default=0)
    current_chapter = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="unread")
    rating = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    authors = db.relationship(
        "Author",
        secondary=book_authors,
        backref=db.backref("books", lazy="dynamic"),
    )
    notes = db.relationship(
        "Note", backref="book", lazy="dynamic", cascade="all, delete-orphan"
    )
    files = db.relationship(
        "File", backref="book", lazy="dynamic", cascade="all, delete-orphan"
    )

    def progress_percentage(self):
        if self.total_pages and self.total_pages > 0:
            return round((self.current_page / self.total_pages) * 100, 1)
        return 0.0

    def to_dict(self, include_authors=False, include_notes=False, include_files=False):
        data = {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "published_date": self.published_date,
            "description": self.description,
            "cover_image": self.cover_image,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
            "total_chapters": self.total_chapters,
            "current_chapter": self.current_chapter,
            "status": self.status,
            "rating": self.rating,
            "progress_percentage": self.progress_percentage(),
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_authors:
            data["authors"] = [a.to_dict() for a in self.authors]
        if include_notes:
            data["notes"] = [n.to_dict() for n in self.notes.all()]
        if include_files:
            data["files"] = [f.to_dict() for f in self.files.all()]
        return data
