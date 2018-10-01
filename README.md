## Bendercoder
[![Build Status](https://travis-ci.org/m19t12/bendercoder.svg?branch=master)](https://travis-ci.org/m19t12/bendercoder)
[![Coverage Status](https://coveralls.io/repos/github/m19t12/bencoder/badge.svg?branch=master)](https://coveralls.io/github/m19t12/bencoder?branch=master)

Library for encoding and decoding bencode data.

## Table of content
- [Introduction](#introduction)
- [Installing](#installing)
- [Usage](#usage)
- [Useful Links](#links)

## Introduction
Bencode (pronounced like B-encode) is the encoding used by the peer-to-peer file sharing system BitTorrent for storing and transmitting loosely structured data.
It supports four different types of values:
- byte strings,
- integers,
- lists,
- dictionaries (associative arrays).

Bencoding is most commonly used in torrent files. These metadata files are simply bencoded dictionaries.

Description from [wikipedia](https://en.wikipedia.org/wiki/Bencode).

## Installing
```
pip install bendercoder
```

## Usage
For decoding and encoding the integer number 10.
```python
# coding=utf-8
from decoder import Decoder
from encoder import Encoder

decoder = Decoder(payload=b'i10e')
decoded_value = decoder.decode()
print(decoded_value)

encoder = Encoder(payload=decoded_value)
encoded_value = encoder.encode()
print(encoded_value)
```
For decoding and encoding the string foo.
```python
# coding=utf-8
from decoder import Decoder
from encoder import Encoder

decoder = Decoder(payload=b'3:foo')
decoded_value = decoder.decode()
print(decoded_value)

encoder = Encoder(payload=decoded_value)
encoded_value = encoder.encode()
print(encoded_value)
```
For decoding and encoding the list [1, 2, 3, 'bar']
```python
# coding=utf-8
from decoder import Decoder
from encoder import Encoder

decoder = Decoder(payload=b'li1ei2ei3e3:bare')
decoded_value = decoder.decode()
print(decoded_value)

encoder = Encoder(payload=decoded_value)
encoded_value = encoder.encode()
print(encoded_value)
```
For decoding and encoding the dictionary {'test': 'foo', 'bar': 2}
```python
# coding=utf-8
from decoder import Decoder
from encoder import Encoder

decoder = Decoder(payload=b'd4:test3:foo3:bari2ee')
decoded_value = decoder.decode()
print(decoded_value)

encoder = Encoder(payload=decoded_value)
encoded_value = encoder.encode()
print(encoded_value)
```

## Links
- [Wikipedia](https://en.wikipedia.org/wiki/Bencode)
- [Theory.org](https://wiki.theory.org/index.php/BitTorrentSpecification)
- [bittorrent.org](http://www.bittorrent.org/beps/bep_0003.html)
