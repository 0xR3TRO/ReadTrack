from database import db
from models.book import Book
from models.author import Author
from utils.validators import validate_required, validate_rating, validate_status


def create_book(user_id, data):
    valid, error = validate_required(data.get("title"), "Title")
    if not valid:
        return None, error

    if data.get("rating") is not None:
        valid, error = validate_rating(data.get("rating"))
        if not valid:
            return None, error

    if data.get("status"):
        valid, error = validate_status(data.get("status"))
        if not valid:
            return None, error

    book = Book(
        title=data["title"],
        genre=data.get("genre"),
        isbn=data.get("isbn"),
        publisher=data.get("publisher"),
        published_date=data.get("published_date"),
        description=data.get("description"),
        cover_image=data.get("cover_image"),
        total_pages=data.get("total_pages", 0),
        current_page=data.get("current_page", 0),
        total_chapters=data.get("total_chapters", 0),
        current_chapter=data.get("current_chapter", 0),
        status=data.get("status", "unread"),
        rating=data.get("rating"),
        user_id=user_id,
    )

    author_ids = data.get("author_ids", [])
    if author_ids:
        authors = Author.query.filter(
            Author.id.in_(author_ids), Author.user_id == user_id
        ).all()
        book.authors = authors

    db.session.add(book)
    db.session.commit()
    return book, None


def get_books(user_id, status=None, search=None):
    query = Book.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    return query.order_by(Book.updated_at.desc()).all()


def get_book(book_id, user_id):
    return Book.query.filter_by(id=book_id, user_id=user_id).first()


def update_book(book_id, user_id, data):
    book = get_book(book_id, user_id)
    if not book:
        return None, "Book not found"

    if "rating" in data and data["rating"] is not None:
        valid, error = validate_rating(data["rating"])
        if not valid:
            return None, error

    if "status" in data:
        valid, error = validate_status(data["status"])
        if not valid:
            return None, error

    for field in [
        "title", "genre", "isbn", "publisher", "published_date",
        "description", "cover_image", "total_pages", "current_page",
        "total_chapters", "current_chapter", "status", "rating",
    ]:
        if field in data:
            setattr(book, field, data[field])

    if "author_ids" in data:
        authors = Author.query.filter(
            Author.id.in_(data["author_ids"]), Author.user_id == user_id
        ).all()
        book.authors = authors

    db.session.commit()
    return book, None


def update_progress(book_id, user_id, data):
    book = get_book(book_id, user_id)
    if not book:
        return None, "Book not found"

    if "current_page" in data:
        page = data["current_page"]
        if page < 0 or (book.total_pages and page > book.total_pages):
            return None, "Invalid page number"
        book.current_page = page

    if "current_chapter" in data:
        chapter = data["current_chapter"]
        if chapter < 0 or (book.total_chapters and chapter > book.total_chapters):
            return None, "Invalid chapter number"
        book.current_chapter = chapter

    if book.total_pages and book.current_page >= book.total_pages:
        book.status = "completed"
    elif book.current_page > 0:
        book.status = "reading"

    db.session.commit()
    return book, None


def delete_book(book_id, user_id):
    book = get_book(book_id, user_id)
    if not book:
        return False, "Book not found"
    db.session.delete(book)
    db.session.commit()
    return True, None
