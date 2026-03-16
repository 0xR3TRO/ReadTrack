from flask import current_app

from database import db
from models.file import File
from models.book import Book
from utils.file_handler import save_file, delete_file as remove_file


def upload_file(user_id, book_id, file_obj):
    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return None, "Book not found"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    result = save_file(file_obj, upload_folder)
    if result is None:
        return None, "Invalid file or file type not allowed"

    unique_filename, original_filename, ext, file_size = result

    file_record = File(
        filename=unique_filename,
        original_filename=original_filename,
        file_type=ext,
        file_size=file_size,
        book_id=book_id,
        user_id=user_id,
    )
    db.session.add(file_record)
    db.session.commit()
    return file_record, None


def get_files(user_id, book_id):
    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return None, "Book not found"
    return book.files.order_by(File.created_at.desc()).all(), None


def get_file(file_id, user_id):
    return File.query.filter_by(id=file_id, user_id=user_id).first()


def delete_file_record(file_id, user_id):
    file_record = get_file(file_id, user_id)
    if not file_record:
        return False, "File not found"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    remove_file(file_record.filename, upload_folder)

    db.session.delete(file_record)
    db.session.commit()
    return True, None
