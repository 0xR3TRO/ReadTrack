import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import models so SQLAlchemy knows about all tables
    from models import User, Book, Author, Note, File  # noqa: F401

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.book_routes import books_bp
    from routes.author_routes import authors_bp
    from routes.note_routes import notes_bp
    from routes.file_routes import files_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(files_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
