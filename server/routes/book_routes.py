from flask import Blueprint
from controllers import book_controller

books_bp = Blueprint("books", __name__, url_prefix="/api/books")

books_bp.add_url_rule("", view_func=book_controller.list_books, methods=["GET"])
books_bp.add_url_rule("", view_func=book_controller.create, methods=["POST"])
books_bp.add_url_rule("/<int:book_id>", view_func=book_controller.get_one, methods=["GET"])
books_bp.add_url_rule("/<int:book_id>", view_func=book_controller.update, methods=["PUT"])
books_bp.add_url_rule("/<int:book_id>", view_func=book_controller.delete, methods=["DELETE"])
books_bp.add_url_rule("/<int:book_id>/progress", view_func=book_controller.progress, methods=["PATCH"])
