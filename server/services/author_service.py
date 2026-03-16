from database import db
from models.author import Author
from utils.validators import validate_required


def create_author(user_id, data):
    valid, error = validate_required(data.get("name"), "Name")
    if not valid:
        return None, error

    author = Author(
        name=data["name"],
        biography=data.get("biography"),
        birth_date=data.get("birth_date"),
        website=data.get("website"),
        user_id=user_id,
    )
    db.session.add(author)
    db.session.commit()
    return author, None


def get_authors(user_id, search=None):
    query = Author.query.filter_by(user_id=user_id)
    if search:
        query = query.filter(Author.name.ilike(f"%{search}%"))
    return query.order_by(Author.name).all()


def get_author(author_id, user_id):
    return Author.query.filter_by(id=author_id, user_id=user_id).first()


def update_author(author_id, user_id, data):
    author = get_author(author_id, user_id)
    if not author:
        return None, "Author not found"

    for field in ["name", "biography", "birth_date", "website"]:
        if field in data:
            setattr(author, field, data[field])

    db.session.commit()
    return author, None


def delete_author(author_id, user_id):
    author = get_author(author_id, user_id)
    if not author:
        return False, "Author not found"
    db.session.delete(author)
    db.session.commit()
    return True, None
