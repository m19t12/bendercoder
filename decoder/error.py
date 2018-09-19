# coding=utf-8
class DecodeError(Exception):
    pass


class InvalidPayload(DecodeError):
    pass


class TokenNotFoundError(DecodeError):
    pass


class ParseValueError(DecodeError):
    pass


class InvalidTokenError(DecodeError):
    pass
