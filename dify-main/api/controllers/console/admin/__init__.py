# Admin controllers package
from functools import wraps
from flask import request
from werkzeug.exceptions import Unauthorized
from configs import dify_config


def admin_required(view):
    @wraps(view)
    def decorated(*args, **kwargs):
        if not dify_config.ADMIN_API_KEY:
            raise Unauthorized("API key is invalid.")

        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            raise Unauthorized("Authorization header is missing.")

        if " " not in auth_header:
            raise Unauthorized("Invalid Authorization header format. Expected 'Bearer <api-key>' format.")

        auth_scheme, auth_token = auth_header.split(None, 1)
        auth_scheme = auth_scheme.lower()

        if auth_scheme != "bearer":
            raise Unauthorized("Invalid Authorization header format. Expected 'Bearer <api-key>' format.")

        if auth_token != dify_config.ADMIN_API_KEY:
            raise Unauthorized("API key is invalid.")

        return view(*args, **kwargs)

    return decorated


__all__ = ['admin_required']
