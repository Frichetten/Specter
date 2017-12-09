# Specter BlockChain Implementation
# Nick Frichette 9/12/2017
"""For now the block chain will be in memory
    At some point, this will get written to 
    disk (I'm not sure what format). Then at 
    startup it will pull the latest blockchain 
    from the nodes in the network"""

from block import *

class Blockchain():
   
    blocks = []

    def __init__(self):
        if len(self.blocks) == 0:
            print 'No blocks in chain'
            print 'Creating Genesis Block'
            genBlock = Block()
            genesis = genBlock.makeGenesisBlock()
            self.addBlock(genesis)

    def addBlock(self, block):
        self.blocks.append(block)

if __name__ == '__main__':
    blockchain = Blockchain()
