#!/usr/bin/env python
# Specter Node
# Nick Frichette 12/9/2017

import argparse

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from node import *
from wallet import *

app = Flask(__name__)

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def receive_tranactions():
    transaction = request.get_json()

    # We just received data from a wallet or node. We now need to
    # package it into a block and add it to the blockchain. First
    # We must validate it.
    if node.authenticate_transaction(transaction):
        if node.validate_transaction(transaction):
            print OK + "Valid Transaction Received" + END
            blockchain.make_block(transaction)
            return "Confirmation"
        else:
            return "Invalid"
    return "Invalid"


@app.route('/getblockchain', methods=['GET'])
def getblockchain():
    return jsonify(blockchain.jsonify())


def print_ascii():
    print " _______  _______  _______  _______ _________ _______  _______      __________    _______"
    print "(  ____ \(  ____ )(  ____ \(  ____ \\\__   __/(  ____ \(  ____ )    /  _    _  \\  /       \\"
    print "| (    \/| (    )|| (    \/| (    \/   ) (   | (    \/| (    )|    | |_|  |_| |  |  BOO  |"
    print "| (_____ | (____)|| (__    | |         | |   | (__    | (____)|    |          |  |  _____/"
    print "(_____  )|  _____)|  __)   | |         | |   |  __)   |     __)    |    __    |  / /"
    print "      ) || (      | (      | |         | |   | (      | (\ (       |   (__)   |   "
    print "/\____) || )      | (____/\| (____/\   | |   | (____/\| ) \ \__    |          |   "
    print "\_______)|/       (_______/(_______/   )_(   (_______/|/   \__/    |/\\/\\/\\/\\/\\|   "


if __name__ == '__main__':
    # Take in CLI Arguments
    parser = argparse.ArgumentParser(description="Node and Web Server for Specter")
    parser.add_argument('-p',
                        metavar='Port Number',
                        help="Run the Web Server on a non-standard port",
                        type=int,
                        default=5000)
    args = parser.parse_args()

    # Print some pretty art
    print "\033[H\033[J\r",
    print_ascii()

    # Spawn out own node and get blockchain
    node = Node()
    blockchain = node.blockchain
    wallet = node.wallet

    if wallet is None:
        print FAIL + 'No wallet detected. Let\'s generate one' + END
        print OK + "Creating nodekey" + END
        wallet = Wallet('nodekey')

    print "Node Wallet Address: " + wallet.get_address()

    app.run(host='0.0.0.0', port=args.p)

