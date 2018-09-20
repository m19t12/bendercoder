# coding=utf-8
from .error import InvalidType


class Encoder:
    __slots__ = ('payload',)

    def __init__(self, payload):
        if type(payload) in (int, str, list, dict):
            self.payload = payload
        else:
            raise InvalidType(
                'Type {} is not supported. Supported types are int, str, list and dict.'.format(type(payload)))

    def encode(self):
        return self.encode_payload(self.payload)

    def encode_payload(self, payload):
        if isinstance(payload, int):
            return self.encode_integer(payload)
        elif isinstance(payload, str) or isinstance(payload, bytes):
            return self.encode_string(payload)
        elif isinstance(payload, list):
            return self.encode_list(payload)
        elif isinstance(payload, dict):
            return self.encode_dictionary(payload)

    @staticmethod
    def encode_integer(payload):
        return str.encode('i{}e'.format(payload))

    @staticmethod
    def encode_string(payload):
        string_length = len(payload)
        return str.encode('{}:{}'.format(string_length, payload))

    def encode_list(self, payload):
        list_items = bytearray('l', 'utf-8')
        list_items += b''.join([self.encode_payload(item) for item in payload])
        list_items += b'e'
        return list_items

    def encode_dictionary(self, payload):
        dict_items = bytearray('d', 'utf-8')
        for key, value in payload.items():
            dict_items += self.encode_payload(key)
            dict_items += self.encode_payload(value)
        dict_items += b'e'
        return dict_items
