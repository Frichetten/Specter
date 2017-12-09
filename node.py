# Specter Node
# Nick Frichette 9/12/2017

import json

from flask import Flask
from flask import jsonify

from blockchain import *


class Node():

    blockchain = None
    app = Flask(__name__)

    def __init__(self):
        # Need to instantiate the Blockchain
        self.blockchain = Blockchain()

    @app.route('/')
    def index(self):
        return "Hello"

    @app.route('/getblockchain', methods=['GET'])
    def getblockchain(self):
        return jsonify(self.blockchain.jsonify())


if __name__ == '__main__':
    node = Node()
    node.app.run()
