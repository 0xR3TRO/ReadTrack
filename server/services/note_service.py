from database import db
from models.note import Note
from models.book import Book
from utils.validators import validate_required


def create_note(user_id, book_id, data):
    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return None, "Book not found"

    valid, error = validate_required(data.get("content"), "Content")
    if not valid:
        return None, error

    note = Note(
        content=data["content"],
        page_number=data.get("page_number"),
        chapter=data.get("chapter"),
        book_id=book_id,
        user_id=user_id,
    )
    db.session.add(note)
    db.session.commit()
    return note, None


def get_notes(user_id, book_id):
    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return None, "Book not found"
    return book.notes.order_by(Note.created_at.desc()).all(), None


def get_note(note_id, user_id):
    return Note.query.filter_by(id=note_id, user_id=user_id).first()


def update_note(note_id, user_id, data):
    note = get_note(note_id, user_id)
    if not note:
        return None, "Note not found"

    for field in ["content", "page_number", "chapter"]:
        if field in data:
            setattr(note, field, data[field])

    db.session.commit()
    return note, None


def delete_note(note_id, user_id):
    note = get_note(note_id, user_id)
    if not note:
        return False, "Note not found"
    db.session.delete(note)
    db.session.commit()
    return True, None
