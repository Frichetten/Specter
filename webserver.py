# Specter Node
# Nick Frichette 9/12/2017

import json

from flask import Flask
from flask import jsonify

from node import *


app = Flask(__name__)

node = Node()
blockchain = node.blockchain


@app.route('/')
def index():
    return "Hello"


@app.route('/getblockchain', methods=['GET'])
def getblockchain():
    return jsonify(blockchain.jsonify())


if __name__ == '__main__':
    app.run()
