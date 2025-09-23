from helper import int_to_little_endian
from Script import Script

class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey
    
    def __repr__(self):
        return f'{self.amount}:{self.script_pubkey}'

    @classmethod
    def parse(cls, stream):
        s_amount = stream.read(8)
        amount = int.from_bytes(s_amount)
        script_pubkey = Script.parse(stream)
        return TxOut(amount, script_pubkey)
    
    def serialize(self):
        '''Returns the byte serialization of the transaction output'''
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result