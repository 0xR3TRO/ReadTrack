from flask import Blueprint
from controllers import file_controller

files_bp = Blueprint("files", __name__, url_prefix="/api/books")

files_bp.add_url_rule("/<int:book_id>/files", view_func=file_controller.list_files, methods=["GET"])
files_bp.add_url_rule("/<int:book_id>/files", view_func=file_controller.upload, methods=["POST"])
files_bp.add_url_rule(
    "/<int:book_id>/files/<int:file_id>", view_func=file_controller.download, methods=["GET"]
)
files_bp.add_url_rule(
    "/<int:book_id>/files/<int:file_id>", view_func=file_controller.delete, methods=["DELETE"]
)
