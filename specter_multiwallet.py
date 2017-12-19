# Specter MultiWallet Implementation
# Nick Frichette 10/12/2017

"""The purpose of the multiwallet is to provide an interface for users
    to interact with their Specter wallets. This application will show
    all the wallets thy currently possess, as well as allow users to
    create more."""

from wallet import *

if __name__ == '__main__':

    wallets = {}

    # The convention for identifying wallets it having the public and
    # private keys in a local directory with the name key-"wallet name"
    for item in os.listdir('.'):
        if 'key-' in item:
            wallets[item[item.index('-')+1:]] = Wallet(item)

    # If there are no keys, then we need to offer the chance to make a wallet
    if len(wallets.keys()) == 0:
        ans = raw_input("We didn't find a wallet, would you like to create one? [y/n]: ")
        if ans == 'y':
            name = raw_input("What would you like to name the wallet?: ")
            print "Creating " + name
        if ans == 'n':
            print "With no keys we'll have to exit. Goodbye"
            exit(0)
