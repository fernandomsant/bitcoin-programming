from helper import hash160, hash256
from S256Point import S256Point
from Signature import Signature
from io import BytesIO
from S256Point import G
from S256Field import S256Field

def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash160(element))

def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(hash256(element))
    return True

def encode_num(num):
    if num == 0:
        return b''
    abs_num = abs(num)
    negative = num < 0
    result = bytearray()
    while abs_num:
        result.append(abs_num & 0xff)
        abs_num >>= 8
    if result[-1] & 0x80:
        if negative:
            result.append(0x80)
        else:
            result.append(0)
    elif negative:
        result[-1] |= 0x80
    return bytes(result)

def decode_num(element):
    if element == b'':
        return 0
    big_endian = element[::-1]
    if big_endian[0] & 0x80:
        negative = True
        result = big_endian[0] & 0x7f
    else:
        negative = False
        result = big_endian[0]
    for c in big_endian[1:]:
        result <<= 8
        result += c
    if negative:
        return -result
    else:
        return result
    
def op_0(stack):
    stack.append(encode_num(0))
    return True

def op_checksig(stack, z):
    if len(stack) < 1:
        return False
    sec_pubkey = stack.pop()
    der_sig = stack.pop()
    pubkey = S256Point.parse(sec_pubkey)
    sig = Signature.parse(BytesIO(der_sig))
    r, s = S256Field(sig.r), S256Field(sig.s)
    if ((z/s)*G + (r/s)*pubkey == S256Point(r, r**3 + pubkey.b, pubkey.a, pubkey.b)):
        return True
    return False

OP_CODE_FUNCTIONS = {
    118: op_dup,
    169: op_hash160,
    170: op_hash256,
}

OP_CODE_NAMES = {
    118: 'OP_DUP',
    169: 'OP_HASH160',
    170: 'OP_HASH256',
}