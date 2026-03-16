from flask import Blueprint
from controllers import note_controller

notes_bp = Blueprint("notes", __name__, url_prefix="/api/books")

notes_bp.add_url_rule("/<int:book_id>/notes", view_func=note_controller.list_notes, methods=["GET"])
notes_bp.add_url_rule("/<int:book_id>/notes", view_func=note_controller.create, methods=["POST"])
notes_bp.add_url_rule(
    "/<int:book_id>/notes/<int:note_id>", view_func=note_controller.update, methods=["PUT"]
)
notes_bp.add_url_rule(
    "/<int:book_id>/notes/<int:note_id>", view_func=note_controller.delete, methods=["DELETE"]
)
