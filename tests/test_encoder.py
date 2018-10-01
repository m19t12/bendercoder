# coding=utf-8
import pytest
from encoder.error import InvalidType


def test_initialize_good_payload(encoder):
    _encoder = encoder(payload='test')
    assert _encoder.payload == 'test'


def test_initialize_bad_payload(encoder):
    with pytest.raises(InvalidType,
                       match="Type <class 'tuple'> is not supported. "
                             "Supported types are int, str, list, bytes and dict."):
        _encoder = encoder(payload=(1, 2))


@pytest.mark.parametrize("payload, expected", [
    (23, b'i23e'),
    (10, b'i10e'),
    (-5, b'i-5e')
])
def test_integer_good_values(payload, expected, encoder):
    _encoder = encoder(payload=payload)
    assert _encoder.encode() == expected


@pytest.mark.parametrize("payload, expected", [
    ('test', b'4:test'),
    ('abcdefg', b'7:abcdefg')
])
def test_string_good_values(payload, expected, encoder):
    _encoder = encoder(payload=payload)
    assert _encoder.encode() == expected


@pytest.mark.parametrize("payload, expected", [
    (b'test', b'4:test'),
    (b'abcdefg', b'7:abcdefg')
])
def test_bytes_good_values(payload, expected, encoder):
    _encoder = encoder(payload=payload)
    assert _encoder.encode() == expected


@pytest.mark.parametrize("payload, expected", [
    ({'test': 'foo', 'bar': 4}, b'd4:test3:foo3:bari4ee'),
    ({'test': [1, 2, 'foo']}, b'd4:testli1ei2e3:fooee')
])
def test_dictionary_good_values(payload, expected, encoder):
    _encoder = encoder(payload=payload)
    assert _encoder.encode() == expected


@pytest.mark.parametrize("payload, expected", [
    ([1, 2, 3], b'li1ei2ei3ee'),
    (['test', 'foo', 'bar'], b'l4:test3:foo3:bare')
])
def test_list_good_values(payload, expected, encoder):
    _encoder = encoder(payload=payload)
    assert _encoder.encode() == expected
