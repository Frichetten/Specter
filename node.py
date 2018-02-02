# Specter Node
# Nick Frichette 12/9/2017


from blockchain import *
from wallet import *

import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Node:

    blockchain = None
    wallet = None

    def __init__(self):
        # Need to instantiate the Blockchain
        self.blockchain = Blockchain(is_node=True)

        # Our node should have its own wallet.
        # The convention for node wallets is different from a
        # standard wallet. Those keys should be in a directory
        # called nodekey. This is because a node should have
        # only one address to mine from. As well as to simplify
        # the issue of having a normal wallet in the same directory.
        for item in os.listdir('.'):
            if 'nodekey' in item:
                self.wallet = Wallet(item)

    def authenticate_transaction(self, transaction):
        is_verified = self.verify_remote_transaction(transaction['from'], transaction['signature'], transaction)
        return is_verified

    def validate_transaction(self, transaction):
        is_validated = self.blockchain.validate_transaction(transaction)
        return is_validated

    def verify_remote_transaction(self, public_key, signature, transaction):
        # transaction.pop('hash')
        transaction = self.wallet.create_signable_transaction(
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


if __name__ == '__main__':
    None
