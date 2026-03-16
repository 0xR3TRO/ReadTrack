from flask import request, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.file_service import upload_file, get_files, get_file, delete_file_record
from utils.responses import success_response, error_response, created_response, no_content_response


@jwt_required()
def list_files(book_id):
    user_id = int(get_jwt_identity())
    files, error = get_files(user_id, book_id)
    if error:
        return error_response(error, status_code=404)
    return success_response(data=[f.to_dict() for f in files])


@jwt_required()
def upload(book_id):
    user_id = int(get_jwt_identity())

    if "file" not in request.files:
        return error_response("No file provided")

    file_obj = request.files["file"]
    file_record, error = upload_file(user_id, book_id, file_obj)
    if error:
        return error_response(error, status_code=404 if "not found" in error.lower() else 400)
    return created_response(data=file_record.to_dict())


@jwt_required()
def download(book_id, file_id):
    user_id = int(get_jwt_identity())
    file_record = get_file(file_id, user_id)
    if not file_record or file_record.book_id != book_id:
        return error_response("File not found", status_code=404)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(
        upload_folder,
        file_record.filename,
        as_attachment=True,
        download_name=file_record.original_filename,
    )


@jwt_required()
def delete(book_id, file_id):
    user_id = int(get_jwt_identity())
    deleted, error = delete_file_record(file_id, user_id)
    if error:
        return error_response(error, status_code=404)
    return no_content_response()
