from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models.user import User
from utils.validators import validate_email, validate_password, validate_username


def register_user(username, email, password):
    valid, error = validate_username(username)
    if not valid:
        return None, error

    valid, error = validate_email(email)
    if not valid:
        return None, error

    valid, error = validate_password(password)
    if not valid:
        return None, error

    if User.query.filter_by(username=username).first():
        return None, "Username already exists"

    if User.query.filter_by(email=email).first():
        return None, "Email already exists"

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return user, None


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return None, "Invalid username or password"
    return user, None


def get_user_by_id(user_id):
    return User.query.get(user_id)
