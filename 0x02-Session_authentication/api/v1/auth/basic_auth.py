#!/usr/bin/env python3
"""basic_auth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """inherits from Auth and defines a BasicAuth
    class
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """returns the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        lst = authorization_header.split()
        if len(lst) != 2:
            return None
        else:
            if lst[0] == 'Basic':
                return lst[1]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """decodes a header to base64
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
        return decoded.decode()

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """ returns the user email and password from the
        Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        lst = decoded_base64_authorization_header.split(':')
        return (lst[0], lst[1])

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        User.load_from_file()
        if User.count() == 0:
            return None
        lst = User.search({'email': user_email})
        if len(lst) == 0:
            return None
        else:
            if not lst[0].is_valid_password(user_pwd):
                return None
            else:
                return lst[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        if header is not None:
            cred = self.extract_base64_authorization_header(header)
            if cred is not None:
                decoded = self.decode_base64_authorization_header(cred)
                if decoded is not None:
                    user = self.extract_user_credentials(decoded)
                    if user[0] is not None and user[1] is not None:
                        return self.user_object_from_credentials(user[0], user[1])
