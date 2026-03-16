from flask import Blueprint
from controllers import author_controller

authors_bp = Blueprint("authors", __name__, url_prefix="/api/authors")

authors_bp.add_url_rule("", view_func=author_controller.list_authors, methods=["GET"])
authors_bp.add_url_rule("", view_func=author_controller.create, methods=["POST"])
authors_bp.add_url_rule("/<int:author_id>", view_func=author_controller.get_one, methods=["GET"])
authors_bp.add_url_rule("/<int:author_id>", view_func=author_controller.update, methods=["PUT"])
authors_bp.add_url_rule("/<int:author_id>", view_func=author_controller.delete, methods=["DELETE"])
