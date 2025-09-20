from hashlib import sha256, new

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def hash256(b):
    return sha256(sha256(b).digest()).digest()

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def hash160(s):
    '''sha256 followed by ripemd160'''
    return new('ripemd160', sha256(s).digest()).digest()