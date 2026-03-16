from flask import jsonify


def success_response(data=None, message=None, status_code=200):
    body = {"success": True}
    if message:
        body["message"] = message
    if data is not None:
        body["data"] = data
    return jsonify(body), status_code


def error_response(message, status_code=400, errors=None):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status_code


def created_response(data=None, message="Created successfully"):
    return success_response(data=data, message=message, status_code=201)


def no_content_response():
    return "", 204
