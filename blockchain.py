# Specter BlockChain Implementation
# Nick Frichette 12/9/2017

import json
import hashlib
import requests
import base64

from threading import Thread

from database_orm import *

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'


class Blockchain:

    NODE_ADDRESS_LIST = ['http://localhost:5000']

    blocks = []
    index = 0
    db = None

    transaction_pool = []

    def __init__(self, is_node=False):

        # Instantiate DB
        self.db = Database()

        if is_node:
            print OK + 'Thank you for standing up a node!' + END

            # If the DB is empty, generate the Genesis
            if self.db.is_empty():
                print FAIL + 'No blocks in chain' + END
                print OK + 'Creating Genesis Block' + END
                genesis = self.make_genesis_block()
                self.add_block(genesis)
                self.db.insert_block(genesis)
            else:
                # For each row in the DB, create a block
                blocks = self.db.get_all_blocks()
                for item in blocks:
                    block = Block(
                        item.coin_index,
                        json.loads(item.transaction_info),
                        item.previous_hash,
                        item.current_hash,
                        item.timestamp,
                        item.nonce
                    )
                    self.add_block(block)

            # Unverified transactions are added to the transaction pool
            # A separate thread will put them onto the block chain.
            # This should be more preformat at scale.
            trans_thread = Thread(target=self.transaction_thread)
            trans_thread.daemon = true
            trans_thread.start()

        else:
            # This is an implementation meant for normal users
            try:
                blockchain_json = self.download_blockchain()
                self.unjsonify(blockchain_json)
            except requests.exceptions.ConnectionError:
                print FAIL + "Failed to connect to nodes. Terminating" + END
                exit()

    def download_blockchain(self):
        # Query the nodes for the blockchain
        # In the future validation will need to occur
        blockchain_json = []
        for address in self.NODE_ADDRESS_LIST:
            request = requests.get(address + '/getblockchain')
            blockchain_json = request.json()
        return blockchain_json

    def update_blockchain(self):
        try:
            blockchain_json = self.download_blockchain()
            self.blocks = []
            self.unjsonify(blockchain_json)
        except requests.exceptions.ConnectionError:
            print "Failed to update blockchain"

    def jsonify(self):
        data_json = {}
        i = 0
        for block in self.blocks:
            data = {
                "index": block.coin_index,
                "transaction": block.transaction_info,
                "previous_hash": block.previous_hash,
                "current_hash": block.current_hash,
                "timestamp": block.timestamp,
                "nonce": block.nonce
            }
            data_json[i] = data
            i += 1
        return data_json

    def unjsonify(self, json_data):
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

            # If not in the DB, insert it
            if not self.db.in_db(block):
                self.db.insert_block(block)

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

    def lookup_address(self, address):
        # Begin searching for transactions from that address
        balance = 0
        for block in self.blocks:
            if block.transaction_info['from'] == address:
                balance -= block.transaction_info['amount']
            if block.transaction_info['to'] == address:
                balance += block.transaction_info['amount']
        return balance

    def validate_transaction(self, transaction):
        # We need to ensure that a transaction is valid on the blockchain
        # First lets get the amount the user wants to move
        amount = int(transaction['amount'])

        # Now let's check their balance with their public key
        balance = self.lookup_address(transaction['from'])

        # Now compare the two
        if amount < balance:
            return True
        else:
            return False

    @staticmethod
    def create_signable_transaction(from_address, to_address, amount, timestamp):
        return ':'.join((from_address, to_address, amount, str(timestamp)))

    def authenticate_transaction(self, transaction):
        is_verified = self.verify_remote_transaction(transaction['from'], transaction['signature'], transaction)
        return is_verified

    def verify_remote_transaction(self, public_key, signature, transaction):
        # transaction.pop('hash')
        transaction = self.create_signable_transaction(
            transaction['from'],
            transaction['to'],
            transaction['amount'],
            transaction['timestamp']
        )

        key = "-----BEGIN PUBLIC KEY-----\n"
        i = 0
        while i < len(public_key):
            key += public_key[i:i+64]+'\n'
            i += 64
        key += "-----END PUBLIC KEY-----\n"

        public_key = serialization.load_pem_public_key(
            str(key),
            backend=default_backend()
        )

        try:
            public_key.verify(
                bytes(base64.decodestring(signature)),
                bytes(transaction),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def transaction_thread(self):
        while true:
            while len(self.transaction_pool) > 0:
                transaction = self.transaction_pool[-1]
                if self.authenticate_transaction(transaction):
                    if self.validate_transaction(transaction):
                        print OK + "Confirmed Transaction" + END
                        self.make_block(self.transaction_pool.pop())

    def add_transaction_to_pool(self, transaction):
        self.transaction_pool.append(transaction)


if __name__ == '__main__':
    blockchain = Blockchain()
