from helper import hash256, int_to_little_endian, encode_varint
from TxOut import TxOut

class Tx:

    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet
    
    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        return f'tx:{self.id()}\nversion {self.version}\ntx_ins:\n{tx_ins}tx_outs:\n{tx_outs}locktime: {self.locktime}'
    
    def id(self):
        '''Human-readable hexadecimal of the transaction hash'''
        return self.hash().hex()
    
    def hash(self):
        '''Binary hash of the legacy serialization'''
        return hash256(self.serialize())[::-1]
    
    # @classmethod
    # def parse(cls, serialization):
    #     version = serialization[0:4]
    # Poderia ser dessa forma, porém estamos lidando com objetos grandes, e o mais apropriado
    # é tratar a transação como um stream de dados

    @classmethod
    def parse(cls, stream, testnet=False):
        # s_ means serialized
        from TxIn import TxIn
        tx_ins, tx_outs = list(), list()
        s_version = stream.read(4)
        version = int.from_bytes(s_version, 'little')
        s_tx_ins_num = stream.read(1)
        tx_ins_num = int.from_bytes(s_tx_ins_num)
        for _ in range(tx_ins_num):
            tx_ins.append(TxIn.parse(stream))
        s_tx_outs_num = stream.read(1)
        tx_outs_num = int.from_bytes(s_tx_outs_num)
        for _ in range(tx_outs_num):
            tx_outs.append(TxOut.parse(stream))
        s_locktime = stream.read(4)
        locktime = int.from_bytes(s_locktime)
        return Tx(version, tx_ins, tx_outs, locktime)
    
    def serialize(self):
        '''Returns the byte serialization of the transaction'''
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result
    
    def fee(self):
        outs = 0
        ins = 0
        for tx_out in self.tx_outs:
            outs += tx_out.amount
        for tx_in in self.tx_ins:
            ins += tx_in.value()
        return ins - outs