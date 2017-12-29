# Specter Node
# Nick Frichette 12/9/2017

from flask import Flask
from flask import jsonify
from flask import request

from node import *
from wallet import *

app = Flask(__name__)

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'


@app.route('/')
def index():
    return "Hello"


@app.route('/', methods=['POST'])
def receive_tranactions():
    transaction = request.get_json()

    # We just received data from a wallet or node. We now need to
    # package it into a block and add it to the blockchain. First
    # We must validate it.
    if validate_transaction(transaction):
        print OK + "Valid Transaction Received" +END
        blockchain.make_block(transaction)
        return "Confirmation"
    else:
        return "Invalid"


@app.route('/getblockchain', methods=['GET'])
def getblockchain():
    return jsonify(blockchain.jsonify())


def validate_transaction(transaction):
    is_verified = wallet.verify_remote_transaction(transaction['from'], transaction['signature'], transaction)
    return is_verified


if __name__ == '__main__':
    # Spawn our own node and get blockchain
    node = Node()
    blockchain = node.blockchain
    wallet = None

    # Our node should have its own wallet.
    # The convention for node wallets is different from a
    # standard wallet. Those keys should be in a directory
    # called nodekey. This is because a node should have
    # only one address to mine from. As well as to simplify
    # the issue of having a normal wallet in the same directory.
    for item in os.listdir('.'):
        if 'nodekey' in item:
            wallet = Wallet(item)

    if wallet is None:
        print FAIL + 'No wallet detected. Let\'s generate one' + END
        print OK + "Creating nodekey" + END
        wallet = Wallet('nodekey')

    print wallet.get_address()

    app.run()

