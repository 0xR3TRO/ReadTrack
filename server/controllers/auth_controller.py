from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from services.auth_service import register_user, authenticate_user, get_user_by_id
from utils.responses import success_response, error_response, created_response


def register():
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    user, error = register_user(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
    )
    if error:
        return error_response(error)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return created_response(
        data={
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        message="Registration successful",
    )


def login():
    data = request.get_json()
    if not data:
        return error_response("Request body is required")

    user, error = authenticate_user(
        username=data.get("username"),
        password=data.get("password"),
    )
    if error:
        return error_response(error, status_code=401)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return success_response(
        data={
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        message="Login successful",
    )


@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return success_response(data={"access_token": access_token})


@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    if not user:
        return error_response("User not found", status_code=404)
    return success_response(data=user.to_dict())
