from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.book_service import (
    create_book,
    get_books,
    get_book,
    update_book,
    update_progress,
    delete_book,
)
from utils.responses import success_response, error_response, created_response, no_content_response


@jwt_required()
def list_books():
    user_id = int(get_jwt_identity())
    status = request.args.get("status")
    search = request.args.get("search")
    books = get_books(user_id, status=status, search=search)
    return success_response(data=[b.to_dict(include_authors=True) for b in books])


@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    book, error = create_book(user_id, data)
    if error:
        return error_response(error)
    return created_response(data=book.to_dict(include_authors=True))


@jwt_required()
def get_one(book_id):
    user_id = int(get_jwt_identity())
    book = get_book(book_id, user_id)
    if not book:
        return error_response("Book not found", status_code=404)
    return success_response(
        data=book.to_dict(include_authors=True, include_notes=True, include_files=True)
    )


@jwt_required()
def update(book_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    book, error = update_book(book_id, user_id, data)
    if error:
        return error_response(error, status_code=404 if "not found" in error.lower() else 400)
    return success_response(data=book.to_dict(include_authors=True))


@jwt_required()
def progress(book_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    book, error = update_progress(book_id, user_id, data)
    if error:
        return error_response(error, status_code=404 if "not found" in error.lower() else 400)
    return success_response(data=book.to_dict())


@jwt_required()
def delete(book_id):
    user_id = int(get_jwt_identity())
    deleted, error = delete_book(book_id, user_id)
    if error:
        return error_response(error, status_code=404)
    return no_content_response()
