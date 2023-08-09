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
        if len(excluded_paths) == 0 and excluded_paths is None:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        """
        return None
