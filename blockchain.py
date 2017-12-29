# Specter BlockChain Implementation
# Nick Frichette 12/9/2017
"""For now the block chain will be in memory
    At some point, this will get written to 
    disk (I'm not sure what format). Then at 
    startup it will pull the latest blockchain 
    from the nodes in the network"""
import json
import hashlib
import requests


from block import *

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'


class Blockchain:
   
    blocks = []
    index = 0
    address_list = ['http://localhost']

    def __init__(self, is_node=False):
        if is_node:
            print OK + 'Thank you for standing up a node!' + END
            print FAIL + 'No blocks in chain' + END
            print OK + 'Creating Genesis Block' + END
            genesis = self.make_genesis_block()
            self.add_block(genesis)
        else:
            # This is an implementation meant for normal users
            try:
                blockchain_json = self.download_blockchain(self.address_list)
                self.unjsonify(blockchain_json)
            except requests.exceptions.ConnectionError:
                print FAIL + "Failed to connect to nodes. Terminating" + END
                exit()

    def download_blockchain(self, address_list):
        # Query the nodes for the blockchain
        # In the future validation will need to occur
        blockchain_json = []
        for address in self.address_list:
            request = requests.get(address + ':5000/getblockchain')
            blockchain_json = request.json()
        return blockchain_json

    def update_blockchain(self):
        try:
            blockchain_json = self.download_blockchain(self.address_list)
            self.unjsonify(blockchain_json)
        except requests.exceptions.ConnectionError:
            print "Failed to update blockchain"

    def jsonify(self):
        data_json = {}
        i = 0
        for block in self.blocks:
            data = {
                "index": block.index,
                "transaction": block.transaction,
                "previous_hash": block.previous_hash,
                "current_hash": block.current_hash,
                "timestamp": block.timestamp,
                "nonce": block.nonce
            }
            data_json[i] = data
            i += 1
        return data_json

    def unjsonify(self, json_data):
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
            self.blocks.append(block)
        return None

    def print_chain(self):
        print self.blocks
        return self.blocks

    def add_block(self, block):
        self.blocks.append(block)

    def make_block(self, transaction):
        self.index += 1

        # Error handling to fix serialization issues
        transaction['amount'] = int(transaction['amount'])

        block_hash = self.calc_block_hash(self.index, transaction['hash'], transaction['timestamp'], transaction, 0)
        block = Block(self.index, transaction, transaction['hash'], block_hash, transaction['timestamp'], 0)
        self.add_block(block)

    def make_genesis_block(self):
        print OK + 'Genesis Block Created' + END
        transaction = {
            "from": "-1",
            "to": "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAupSwIG17vricebp6EN88"+ 
                  "7wzHj0OsaxYl24z2VT6U9+ByEoGGWOPC/Nv9jwebzCLT49Bv5nZL0c7WCQMvvb5o"+
                  "3BNk2wPZR6XEQBZxgwXJdt5h2Ye+Nyc8wYvZodp1ouUv2jCNvcnH4VCz6y56yPzc"+
                  "861ZeYGGO9xbTu7RLkBqGODIqNqLzRhIdpYDukz2TVgHrEXalu+SFkrHo+oc5OBg"+
                  "YYLQeOSlzRKxgfvFG9ViNlqHP0tQDQsGnakBFuBWW5DuwrEKjqkmM+dxo9ALNaag"+
                  "ELpB60zXK2ZxwdvOmko8KZNsHVQMzZql2hcJiyfc99OvOBgp/xTscK94NNqQ6m2M"+
                  "pFr8V07XFnRB8r1EQhY9oFuraUi9xSZbKc3DVG3FEfSyo2Q/+jT+9dkSt7GegIya"+
                  "wM3saOY2VeN1f8XsfQ+a96SL+ltas99NlDJGMuOJOjrKherpfEBcuEK5EvljceGy"+
                  "b7O4NyUcQ/k0q/ngQM+Lz5/3RUShqCbtkmjH5FAxiNHzluy83hJyxGxrYHTEMF88"+
                  "Z6YHyaOBUpMp3mvPMVqM/jeI2aslJDTEDmeaRhs6yI90RDyohzb1FUctUKVPiL8a"+
                  "FI9/gKmSCpgB8BEpI23K0az4kbItnWLe3xzABSFL0nSQWkXQqWmepKcDwp6TcJtG"+
                  "/U5BSE284qlQFOd50rW0xRUCAwEAAQ==",
            "amount": 10,
            "signature": "-1",
            "timestamp": -1,
            "hash": -1
        }
        current_hash = self.calc_block_hash(0, -1, -1, transaction, 0)
        genesis_block = Block(0, transaction, -1, current_hash, 0, 0)
        self.index += 1
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
