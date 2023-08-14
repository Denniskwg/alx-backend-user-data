#!/usr/bin/env python3
"""session_auth
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ handles all routes for the Session authentication
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    lst = User.search({'email': email})
    if len(lst) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        if not lst[0].is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(getattr(lst[0], 'id'))
            key = getenv('SESSION_NAME', None)
            user_dict = jsonify(lst[0].to_json())
            if key is not None:
                user_dict.set_cookie(key, session_id)
                return user_dict
