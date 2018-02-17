## Dependencies
* Pip           (Depends on your operating system)
* Cryptography  (sudo pip install cryptography)
* Flask         (sudo pip install flask)
* SQLAlchemy    (sudo pip install sqlalchemy)

## How To Install and Run Specter
Please be aware that Specter uses Python 2.7. This may change in the future, but for right now that is what we are using.

Installing Specter is rather easy depending on your operating system.

* First: Install Pip (Depends on your operating system, see [this](https://pip.pypa.io/en/stable/installing/))
* Second: Be sure to install all the dependencies above (Those commands should help you install)
* Third: Clone the repo to your local machine (git clone https://github.com/Frichetten/Specter.git)
* Fourth: Run the webserver.py first so that you have a local node. (python webserver.py)
* Fifth: Run the multiwallet.py to create a wallet. (python multiwallet.py)

## Detailed Explanation
Blockchain technology is a designed to be a distributed ledger (generally). As a result, in order to interact with, or build a blockchain you need what is called a node. This node (and future ones) will be responsible for collecting transactions and verifying them within the network. Whenever you are testing Specter, you need to first run the webserver.py which is a webserver implementation of the node. Then, you can interact with it using the multiwallet tool which will allow you to create wallets and interact with the blockchain. 

**Have any questions or run into any issues? Feel free to mention that in the Issue Tracker near the top of the page.**
