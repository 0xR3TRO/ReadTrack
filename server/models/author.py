from datetime import datetime, timezone

from database import db


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    biography = db.Column(db.Text, nullable=True)
    birth_date = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self, include_books=False):
        data = {
            "id": self.id,
            "name": self.name,
            "biography": self.biography,
            "birth_date": self.birth_date,
            "website": self.website,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_books:
            data["books"] = [b.to_dict() for b in self.books.all()]
        return data
