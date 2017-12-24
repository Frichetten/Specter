# Specter MultiWallet Implementation
# Nick Frichette 12/10/2017

"""The purpose of the multiwallet is to provide an interface for users
    to interact with their Specter wallets. This application will show
    all the wallets thy currently possess, as well as allow users to
    create more."""

from wallet import *
from blockchain import *

if __name__ == '__main__':

    wallets = {}
    blockchain = Blockchain()

    # The convention for identifying wallets it having the public and
    # private keys in a local directory with the name key-"wallet name"
    for item in os.listdir('.'):
        if 'key-' in item and 'nodekey' not in item:
            wallets[item[item.index('-')+1:]] = Wallet(item)

    # If there are no keys, then we need to offer the chance to make a wallet
    if len(wallets.keys()) == 0:
        ans = raw_input("We didn't find a wallet, would you like to create one? [y/n]: ")
        if ans == 'y':
            name = raw_input("What would you like to name the wallet?: ")
            print "Creating " + name
            wallets['key-' + name] = Wallet(name)
        if ans == 'n':
            print "With no keys we'll have to exit. Goodbye"
            exit(0)

    """ Now that we've loaded the wallets, lets give the users some choices """
    ans = ""
    while ans != 'exit':
        print "Welcome to Specter Multi_Wallet V0.02"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print ""
        print "To begin, select a wallet listed below"
        print ""
        for i, item in enumerate(wallets.keys()):
            print "("+str(i)+") " + wallets[item].name
        
        ans = raw_input(">> ")
