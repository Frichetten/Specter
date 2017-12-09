# Specter Block Implementation
# Nick Frichette 9/12/2017

class Block():

    def makeGenesisBlock(self):
        transaction = {
            "from": "-1",
            "to" : "-1",
            "amount": 10,
            "signature": "-1",
            "timestamp": -1,
            "hash" : -1
        }
        return transaction

if __name__ == '__main__':
    None
