# coding=utf-8
"""Bencoder main decode class implementation.

Copyright (C) 2018  Manolis Tsoukalas.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""
from decoder.error import ParseValueError, TokenNotFoundError, InvalidTokenError, InvalidPayload

# Token that indicates end of list, dictionary and integer.
TOKEN_END = b'e'

# Token that indicates start of integer.
TOKEN_INTEGER = b'i'

# Token that indicates separation of string length and string data.
TOKEN_STRING_SEPARATOR = b':'

# Token that indicates start of dictionary.
TOKEN_DICTIONARY = b'd'

# Token that indicates start of list.
TOKEN_LIST = b'l'


class Decoder:
    """
    Decoder main class for decoding bencode data.

    Example:
        >>>> decoder = Decoder(b'i10e')
        .... value = decoder.decode()
        value now is 10 integer.
    """
    __slots__ = ('payload', 'index')

    def __init__(self, payload):
        if not isinstance(payload, bytes):
            raise InvalidPayload('Payload data must be of type bytes')
        self.payload = payload
        self.index = 0

    def decode(self):
        """
        Decodes the payload and returns a python related object.
        :return: Python object
        """
        decode_type = self.get_type()

        if decode_type == TOKEN_INTEGER:
            self.index += 1
            return self.decode_integer()
        elif decode_type == TOKEN_LIST:
            self.index += 1
            return self.decode_list()
        elif decode_type == TOKEN_DICTIONARY:
            self.index += 1
            return self.decode_dict()
        elif decode_type.isdigit():
            return self.decode_string()
        else:
            raise InvalidTokenError('Decode type {} is not supported'.format(decode_type))

    def get_type(self):
        decode_type = self.payload[self.index: self.index + 1]
        return decode_type

    def decode_dict(self):
        dictionary_value = {}

        while self.payload[self.index: self.index + 1] != b'e':
            dictionary_value.update({
                self.decode(): self.decode()
            })
        self.index += 1
        return dictionary_value

    def decode_list(self):
        list_values = []

        while self.payload[self.index: self.index + 1] != b'e':
            list_values.append(self.decode())

        self.index += 1

        return list_values

    def decode_integer(self):
        try:
            hit = self.payload.index(TOKEN_END, self.index)
        except ValueError:
            raise TokenNotFoundError("Token {} not found".format(TOKEN_END))

        try:
            value = int(self.payload[self.index: hit])
        except ValueError:
            raise ParseValueError("Can't parse value {} to integer".format(self.payload[self.index: hit]))

        self.index = hit + 1

        return value

    def decode_string(self):
        try:
            hit = self.payload.index(TOKEN_STRING_SEPARATOR, self.index)
        except ValueError:
            raise TokenNotFoundError("Token {} not found".format(TOKEN_STRING_SEPARATOR))

        try:
            string_length = int(self.payload[self.index: hit])
        except ValueError:
            raise ParseValueError(
                "Can't parse value for string size {} to integer".format(self.payload[self.index: hit]))

        self.index = hit + 1

        try:
            # if value can be decoded in utf-8 it means it is a string
            value = self.payload[self.index:self.index + string_length].decode('utf-8')
        except UnicodeDecodeError:
            # if can't be decode it means is a byte representation (SHA1 hash values)
            value = self.payload[self.index:self.index + string_length]

        self.index += string_length

        return value
