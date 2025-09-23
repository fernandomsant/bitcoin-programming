class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s
    
    def __repr__(self):
        return f'Signature({self.r}, {self.s})'
    
    def der(self):
        rbin = self.r.to_bytes(32, byteorder='big')
        rbin = rbin.lstrip(b'\x00')
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, byteorder='big')
        sbin = sbin.lstrip(b'\x00')
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result
    
    @classmethod
    def parse(cls, stream):
        stream.read(3)
        rlen = int.from_bytes(stream.read(1))
        r = int.from_bytes(stream.read(rlen), 'big')
        stream.read(1)
        slen = int.from_bytes(stream.read(1))
        s = int.from_bytes(stream.read(slen))
        return Signature(r, s)