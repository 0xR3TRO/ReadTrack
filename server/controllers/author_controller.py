from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.author_service import (
    create_author,
    get_authors,
    get_author,
    update_author,
    delete_author,
)
from utils.responses import success_response, error_response, created_response, no_content_response


@jwt_required()
def list_authors():
    user_id = int(get_jwt_identity())
    search = request.args.get("search")
    authors = get_authors(user_id, search=search)
    return success_response(data=[a.to_dict() for a in authors])


@jwt_required()
def create():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    author, error = create_author(user_id, data)
    if error:
        return error_response(error)
    return created_response(data=author.to_dict())


@jwt_required()
def get_one(author_id):
    user_id = int(get_jwt_identity())
    author = get_author(author_id, user_id)
    if not author:
        return error_response("Author not found", status_code=404)
    return success_response(data=author.to_dict(include_books=True))


@jwt_required()
def update(author_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    author, error = update_author(author_id, user_id, data)
    if error:
        return error_response(error, status_code=404 if "not found" in error.lower() else 400)
    return success_response(data=author.to_dict())


@jwt_required()
def delete(author_id):
    user_id = int(get_jwt_identity())
    deleted, error = delete_author(author_id, user_id)
    if error:
        return error_response(error, status_code=404)
    return no_content_response()
