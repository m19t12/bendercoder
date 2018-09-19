# coding=utf-8
import pytest
from decoder import Decoder


@pytest.fixture(scope='session')
def decoder():
    return Decoder
