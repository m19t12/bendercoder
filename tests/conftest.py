# coding=utf-8
import pytest
from decoder import Decoder
from encoder import Encoder


@pytest.fixture(scope='session')
def decoder():
    return Decoder


@pytest.fixture(scope='session')
def encoder():
    return Encoder
