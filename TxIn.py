from helper import int_to_little_endian
from TxFetcher import TxFetcher
from Script import Script

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence
    
    def __repr__(self):
        return f'{self.prev_tx.hex()}:{self.prev_index}'
    
    @classmethod
    def parse(cls, stream):
        s_tx_id = stream.read(32)
        s_tx_index = stream.read(4)
        tx_index = int.from_bytes(s_tx_index, 'little')
        s_script_sig_len = stream.read(1)
        script_sig_len = int.from_bytes(s_script_sig_len)
        s_script_sig = stream.read(script_sig_len)
        script_sig = int.from_bytes(s_script_sig)
        s_sequence = stream.read(4)
        sequence = int.from_bytes(s_sequence)
        return TxIn(s_tx_id, tx_index, script_sig, sequence)
    
    def serialize(self):
        '''Returns the byte serialization of the transaction input'''
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result
    
    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        '''Get the output value by looking up the tx hash.
        Returns the amount in satoshi'''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount
    
    def script_pubkey(self, testnet=False):
        '''Get the ScriptPubKey by looking up the tx hash.
        Returns a Script object'''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey