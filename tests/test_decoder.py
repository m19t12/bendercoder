# coding=utf-8
import pytest
from decoder.error import TokenNotFoundError, ParseValueError, InvalidPayload, InvalidTokenError


def test_initialization_good_payload(decoder):
    _decoder = decoder(b'i123e')
    assert _decoder.payload == b'i123e'


def test_initialization_bad_payload(decoder):
    with pytest.raises(InvalidPayload, match='Payload data must be of type bytes'):
        _decoder = decoder('123')


def test_type_checking_bad_payload(decoder):
    _decoder = decoder(b'a1234e')
    with pytest.raises(InvalidTokenError, match="Decode type b'a' is not supported"):
        _decoder.decode()


@pytest.mark.parametrize("payload, expected", [
    (b'i345e', 345),
    (b'i10e', 10),
    (b'i1e', 1),
    (b'i999999999999e', 999999999999)
])
def test_good_values_integer_payload(payload, expected, decoder):
    _decoder = decoder(payload=payload)
    assert _decoder.decode() == expected


def test_integer_payload_token_not_found_error(decoder):
    _decoder = decoder(payload=b'i1234')
    with pytest.raises(TokenNotFoundError, match="Token b'e' not found"):
        _decoder.decode()


def test_integer_payload_parse_value_error(decoder):
    _decoder = decoder(payload=b'i1234abce')
    with pytest.raises(ParseValueError, match="Can't parse value b'1234abc' to integer"):
        _decoder.decode()


@pytest.mark.parametrize("payload, expected", [
    (b'4:abcd', 'abcd'),
    (b'4:test', 'test'),
    (b'3:foo', 'foo'),
    (b'3:barfoo', 'bar'),
    (b'0:a', ''),
    (b'0:', '')
])
def test_string_good_payload(payload, expected, decoder):
    _decoder = decoder(payload=payload)
    assert _decoder.decode() == expected


def test_string_payload_token_not_found_error(decoder):
    _decoder = decoder(payload=b'4abcd')
    with pytest.raises(TokenNotFoundError, match="Token b':' not found"):
        _decoder.decode()


def test_string_payload_parse_string_length_value_error(decoder):
    _decoder = decoder(payload=b'4a:abcd')
    with pytest.raises(ParseValueError, match="Can't parse value for string size b'4a' to integer"):
        _decoder.decode()


def test_string_byte_sha1_byte(decoder):
    _decoder = decoder(payload=b'74520:\xba \xb5\xa7-0%\xbb')
    assert _decoder.decode() == b'\xba \xb5\xa7-0%\xbb'


@pytest.mark.parametrize("payload, expected", [
    (b'li32ee', [32]),
    (b'l4:testee', ['test']),
    (b'l4:eeeee', ['eeee'])
])
def test_list_good_payload(payload, expected, decoder):
    _decoder = decoder(payload=payload)
    assert _decoder.decode() == expected


def test_list_bad_end_payload(decoder):
    _decoder = decoder(payload=b'li34e')
    with pytest.raises(InvalidTokenError, match="Decode type b'' is not supported"):
        _decoder.decode()


@pytest.mark.parametrize("payload, expected", [
    (b'd4:test3:fooe', {'test': 'foo'}),
    (b'd3:bari20ee', {'bar': 20}),
    (b'd3:bazli10ei5eee', {'baz': [10, 5]})
])
def test_dictionary_good_payload(payload, expected, decoder):
    _decoder = decoder(payload=payload)
    assert _decoder.decode() == expected


def test_dictionary_bad_payload(decoder):
    _decoder = decoder(payload=b'd4:testli20ee')
    with pytest.raises(InvalidTokenError, match="Decode type b'' is not supported"):
        _decoder.decode()
