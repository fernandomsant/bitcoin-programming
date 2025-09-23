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

def int_to_little_endian(n: int, length: int) -> bytes:
    base = 0xff + 1
    result = b''
    q, r = divmod(n, base)
    while True:
        result += r.to_bytes()
        if q == 0:
            break
        q, r = divmod(q, base)
    if length < len(result):
        raise OverflowError('int too big to convert')
    result += b'\x00' * (length - len(result))
    return result

def little_endian_to_int(b: bytes) -> int:
    result = 0
    for p, byte in enumerate(b):
        result += byte * (256**p)
    return result

def read_varint(s):
    '''read_varint reads a variable integer from a stream'''
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else is just the integer
        return i
    
def encode_varint(i):
    '''encodes an integer as a varint'''
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError(f'integer too large: {i}')