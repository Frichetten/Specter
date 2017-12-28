# Specter Wallet Implementation
# Nicholas Frichette 12/8/2017
import os
import requests

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from blockchain import *

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'

class Wallet:

    NODE_ADDRESS_LIST = ['http://localhost']

    name = ""
    publicKey = ""
    privateKey = ""
    balance = 0

    def __init__(self, wallet_name):
        # Determine if keys are present
        if not self.find_keys(wallet_name):

            wallet_name = 'key-'+wallet_name

            # Make the directory for the keys
            os.mkdir(wallet_name)

            # Generate and serialize private key
            private_key = self.generate_private_key()
            private_pem = self.serialize_private_key(private_key)
            self.write_key(wallet_name+'/Private', private_pem)

            # Generate and serialize public key
            public_key = private_key.public_key()
            print OK + 'Generated Public Key' + END
            public_pem = self.serialize_public_key(public_key)
            self.write_key(wallet_name+'/Public', public_pem)

        print OK + 'Key\'s found!: ' + wallet_name + END

        # Set the name
        self.name = wallet_name[4:]

        # Load keys
        self.publicKey = self.load_key(wallet_name + '/Public')
        self.privateKey = self.load_key(wallet_name + '/Private')

        # Here we would do one of two things. Either we would load our
        # current blockchain from disk and then download anything we
        # are missing, or we would download the whole thing if we didn't
        # previously have it downloaded. Because we are still a prototype
        # we will always download the whole wallet at startup.

        """ The following is outdated logic. A wallet should not maintain a full copy of the 
            block chain. This doesn't make any sense if you consider having multiple wallets.
            Each wallet tracking their own blockchain would become expensive quickly. Instead 
            the application running the wallets (wether that is the multiwallet or the node 
            itself) should handle the blockcahin. """

        # Download the blockchain from localhost
        #try:
        #    blockchain_json = self.download_blockchain(self.NODE_ADDRESS_LIST)
        #    self.blockchain = Blockchain.unjsonify(blockchain_json)
        #except requests.exceptions.ConnectionError:
        #    print FAIL + 'Failed to connect to nodes. Terminating.' + END
        #    exit(1)

        # Now that we have the blockchain we need to determine our balance
        #self.balance = self.get_balance(self.get_address())

    def display_address_and_balance(self):
        print "Wallet Address:", self.get_address()[:20] + "..."
        print "Balance:", self.get_balance(self.get_address())

    def get_balance(self, address, blockchain):
        balance = 0
        for block in blockchain.blocks:
            if block.transaction['from'] == address:
                balance -= block.transaction['amount']
            if block.transaction['to'] == address:
                balance += block.transaction['amount']
        return balance

    def get_address(self):
        address = self.serialize_public_key(self.publicKey)
        return ''.join(address.split('\n')[1:-2])

    def verify_transaction(self, signature, transaction):
        verification = self.publicKey.verify(
            signature,
            transaction,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return verification

    def sign_transaction(self, transaction):
        signature = self.privateKey.sign(
            transaction,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def load_key(self, name):
        if 'Public' in name:
            with open(name + '.key', 'rb') as key:
                key = serialization.load_pem_public_key(
                    key.read(),
                    backend=default_backend()
                )
        elif 'Private' in name:
            with open(name + '.key', 'rb') as key:
                key = serialization.load_pem_private_key(
                    key.read(),
                    password=None,
                    backend=default_backend()
                )
        return key

    def write_key(self, name, key):
        print 'Writing ' + name + ' Key to ./' + name + '.key'
        with open(name + '.key', 'w') as f:
            for line in key.splitlines():
                f.write(line + '\n')
        print OK + 'Wrote ' + name + ' key to file' + END

    def generate_private_key(self):
        print 'Generating a Private Key'
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        print OK + 'Generated Private Key' + END
        return private_key

    def serialize_private_key(self, private_key):
        privatePEM = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        print OK + 'Serialized Private Key' + END
        return privatePEM

    def serialize_public_key(self, public_key):
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print OK + 'serialized Public Key' + END
        return public_pem

    def find_keys(self, wallet_name):
        try:
            directory = os.listdir(wallet_name)
            if 'Private.key' not in directory \
                    or 'Public.key' not in directory:
                        return False
            return True
        except OSError as e:
            return False


if __name__ == '__main__':
    pass
