# Specter Node
# Nick Frichette 9/12/2017

from flask import Flask

from blockchain import *

class Node():

    blockchain = None
    app = Flask(__name__)

    def __init__(self):
        # Need to instantiate the Blockchain
        self.blockchain = Blockchain()

    @app.route('/')
    def index():
        return "Hello"

if __name__ == '__main__':
    node = Node()
    node.app.run()
