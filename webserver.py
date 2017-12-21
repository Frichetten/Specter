# Specter Node
# Nick Frichette 12/9/2017

from flask import Flask
from flask import jsonify

from node import *
from wallet import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello"


@app.route('/getblockchain', methods=['GET'])
def getblockchain():
    return jsonify(blockchain.jsonify())


if __name__ == '__main__':
    # Spawn our own node and get blockchain
    node = Node()
    blockchain = node.blockchain

    # Our node should have its own wallet.
    # The convention for node wallets is different from a
    # standard wallet. Those keys should be in a directory
    # called nodekey. This is because a node should have
    # only one address to mine from. As well as to simplify
    # the issue of having a normal wallet in the same directory.
    wallet = None
    for item in os.listdir('.'):
        if 'nodekey' in item:
            wallet = Wallet(item)

    if wallet is None:
        print 'No wallet detected. Exiting'
        exit()

    app.run()

