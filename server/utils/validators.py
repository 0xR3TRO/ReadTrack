import re


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not email or not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None


def validate_password(password):
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, None


def validate_username(username):
    if not username or len(username) < 3 or len(username) > 80:
        return False, "Username must be between 3 and 80 characters"
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    return True, None


def validate_required(value, field_name):
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return False, f"{field_name} is required"
    return True, None


def validate_rating(rating):
    if rating is None:
        return True, None
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return False, "Rating must be between 1 and 5"
    return True, None


def validate_status(status):
    valid_statuses = ["unread", "reading", "completed", "on_hold"]
    if status and status not in valid_statuses:
        return False, f"Status must be one of: {', '.join(valid_statuses)}"
    return True, None
