# Specter Wallet Implementation
# Nicholas Frichette 8/12/2017
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'

class Wallet:

    publicKey = ""
    privateKey = ""

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

                public_key = private_key.public_key()
                publicPEM = public_key.public_bytes(
                    encoding = serialization.Encoding.PEM,
                    format = serialization.PublicFormat.SubjectPublicKeyInfo
                )
                print OK + 'Generated Public Key' + END

    
    def writeKey(self, name, key):
        print 'Writing ' + name + ' Key to ./' + name + '.key'


    
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


    def findKeys(self):
        directory = os.listdir('.')
        if 'private.key' not in directory \
            or 'public.key' not in directory: 
                return False
        return True

if __name__ == '__main__':
    wallet = Wallet()
