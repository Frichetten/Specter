# Specter Wallet Implementation
# Nicholas Frichette 8/12/2017
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'

class Wallet:

    publicKey = ""
    privateKey = ""
    value = 0

    def __init__(self):
        print 'Instantiating Wallet'

        # Determine if keys are present
        if not self.findKeys():
            print FAIL + 'No keys were found' + END
            ans = raw_input('Would you like to generate ' + \
                    'a public/private key pair? (y/n): ')

            if ans.lower() == 'n':
                print 'Without a key, we can\'t do anything'
                print FAIL + 'Terminating Wallet' + END
                quit()
            elif ans.lower() == 'y':
                # Generate and serialize private key
                private_key = self.generatePrivateKey()
                privatePEM = self.serializePrivateKey(private_key)
                self.writeKey('Private', privatePEM)

                #Generate and serialize public key
                public_key = private_key.public_key()
                print OK + 'Generated Public Key' + END
                publicPEM = self.serializePublicKey(public_key)                
                self.writeKey('Public', publicPEM)

        print 'Key\'s found!'
        # load public key
        self.publicKey = self.loadKey('Public')
        self.privateKey = self.loadKey('Private')


    def verifyTransaction(self, signature, transaction):
        verification = self.publicKey.verify(
            signature,
            transaction,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return verification


    def signTransaction(self, transaction):
        signature = self.privateKey.sign(
            transaction,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature


    def loadKey(self, name):
        if name == 'Public':
            with open('./' + name + '.key', 'rb') as key:
                key = serialization.load_pem_public_key(
                    key.read(),
                    backend = default_backend()
                )
        elif name == 'Private':
            with open('./' + name + '.key', 'rb') as key:
                key = serialization.load_pem_private_key(
                    key.read(),
                    password = None,
                    backend = default_backend()
                )
        return key

    
    def writeKey(self, name, key):
        print 'Writing ' + name + ' Key to ./' + name + '.key'
        with open(name + '.key', 'w') as f:
            for line in key.splitlines():
                f.write(line + '\n')
        print OK + 'Wrote ' + name + ' key to file' + END

    
    def generatePrivateKey(self):
        print 'Generating a Private Key'
        private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 4096,
            backend = default_backend()
        )
        print OK + 'Generated Private Key' + END
        return private_key


    def serializePrivateKey(self, private_key):
        privatePEM = private_key.private_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm = serialization.NoEncryption()
        )
        print OK + 'Serialized Private Key' + END
        return privatePEM

    
    def serializePublicKey(self, public_key):
        publicPEM = public_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print OK + 'Serialized Public Key' + END
        return publicPEM


    def findKeys(self):
        directory = os.listdir('.')
        if 'Private.key' not in directory \
            or 'Public.key' not in directory: 
                return False
        return True

if __name__ == '__main__':
    wallet = Wallet()
