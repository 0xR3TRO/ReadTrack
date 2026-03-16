import os
import uuid

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "txt", "doc", "docx", "epub", "mobi", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, upload_folder):
    if not file or file.filename == "":
        return None
    if not allowed_file(file.filename):
        return None

    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)

    file_size = os.path.getsize(filepath)
    return unique_filename, original_filename, ext, file_size


def delete_file(filename, upload_folder):
    filepath = os.path.join(upload_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
