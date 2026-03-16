from datetime import datetime, timezone

from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    books = db.relationship(
        "Book", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )
    notes = db.relationship(
        "Note", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )
    authors = db.relationship(
        "Author", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )
    files = db.relationship(
        "File", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
