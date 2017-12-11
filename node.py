# Specter Node
# Nick Frichette 9/12/2017


from blockchain import *


class Node:

    blockchain = None

    def __init__(self):
        # Need to instantiate the Blockchain
        self.blockchain = Blockchain()


if __name__ == '__main__':
    None
