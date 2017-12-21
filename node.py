# Specter Node
# Nick Frichette 12/9/2017


from blockchain import *


class Node:

    blockchain = None

    def __init__(self):
        # Need to instantiate the Blockchain
        self.blockchain = Blockchain()


if __name__ == '__main__':
    None
