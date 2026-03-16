from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.note_service import create_note, get_notes, update_note, delete_note
from utils.responses import success_response, error_response, created_response, no_content_response


@jwt_required()
def list_notes(book_id):
    user_id = int(get_jwt_identity())
    notes, error = get_notes(user_id, book_id)
    if error:
        return error_response(error, status_code=404)
    return success_response(data=[n.to_dict() for n in notes])


@jwt_required()
def create(book_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    note, error = create_note(user_id, book_id, data)
    if error:
        return error_response(error, status_code=404 if "not found" in error.lower() else 400)
    return created_response(data=note.to_dict())


@jwt_required()
def update(book_id, note_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    note, error = update_note(note_id, user_id, data)
    if error:
        return error_response(error, status_code=404 if "not found" in error.lower() else 400)
    return success_response(data=note.to_dict())


@jwt_required()
def delete(book_id, note_id):
    user_id = int(get_jwt_identity())
    deleted, error = delete_note(note_id, user_id)
    if error:
        return error_response(error, status_code=404)
    return no_content_response()
