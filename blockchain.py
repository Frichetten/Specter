# Specter BlockChain Implementation
# Nick Frichette 9/12/2017
"""For now the block chain will be in memory
    At some point, this will get written to 
    disk (I'm not sure what format). Then at 
    startup it will pull the latest blockchain 
    from the nodes in the network"""

from block import *


class Blockchain:
   
    blocks = []

    def __init__(self, copy=None):
        if len(self.blocks) == 0 and copy is None:
            print 'No blocks in chain'
            print 'Creating Genesis Block'
            genesis = self.make_genesis_block()
            self.add_block(genesis)
        else:
            self.add_block(copy)

    def jsonify(self):
        data_json = {}
        i = 0
        for block in self.blocks:
            data = {
                "index": block.index,
                "transaction": block.index,
                "previous_hash": block.previous_hash,
                "current_hash": block.current_hash,
                "timestamp": block.timestamp,
                "nonce": block.nonce
            }
            data_json[i] = data
            i += 1
        return data_json

    @staticmethod
    def unjsonify(json_data):
        blockc = None
        for block in json_data:
            js = json_data[block]
            block = Block(
                js['index'],
                js['transaction'],
                js['previous_hash'],
                js['current_hash'],
                js['timestamp'],
                js['nonce']
            )
            if blockc is None:
                blockc = Blockchain(block)
            else:
                blockc.add_block(block)
        return blockc

    def print_chain(self):
        return self.blocks

    def make_genesis_block(self):
        print 'Genesis Block Created'
        transaction = {
            "from": "-1",
            "to": "-1",
            "amount": 10,
            "signature": "-1",
            "timestamp": -1,
            "hash": -1
        }
        current_hash = self.calc_block_hash(0, -1, -1, transaction, 0)
        genesis_block = Block(0, transaction, -1, current_hash, 0, 0)
        return genesis_block

    def calc_block_hash(self, index, prev_hash, timestamp, transaction, nonce=0):
        data = {
            "index": index,
            "previous_hash": prev_hash,
            "timestamp": timestamp,
            "transaction": transaction,
            "nonce": nonce
        }
        data_json = json.dumps(data, sort_keys=True)
        hashed = hashlib.sha256(data_json)
        return hashed.hexdigest()

    def add_block(self, block):
        self.blocks.append(block)


if __name__ == '__main__':
    blockchain = Blockchain()
