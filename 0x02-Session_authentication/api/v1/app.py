#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


@app.before_request
def before_each_request():
    """called before each request
    """
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    paths.append('/api/v1/auth_session/login/')
    if auth:
        if auth.require_auth(request.path, paths):
            res1 = auth.session_cookie(request)
            res2 = auth.authorization_header(request)
            if res1 is None and res2 is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)
            else:
                request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    var = getenv("AUTH_TYPE", None)
    if var == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    if var == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    if var == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    app.run(host=host, port=port)
