# Specter Node
# Nick Frichette 12/9/2017


from blockchain import *
from wallet import *


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


if __name__ == '__main__':
    None
