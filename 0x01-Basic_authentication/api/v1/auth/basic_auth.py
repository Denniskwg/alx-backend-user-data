#!/usr/bin/env python3
"""basic_auth
"""
from api.v1.auth.auth import Auth
import base64


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
        except base64.binascii.Error:
            return None
        return decoded.decode()
