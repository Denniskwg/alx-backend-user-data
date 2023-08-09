#!/usr/bin/env python3
"""auth defines a class Auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """defines an authentication class for an api
    """
    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns None if request is None or if request
        doesnt contain Authorization
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers.keys():
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        """
        return None
