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

    print wallets['First Wallet'].balance
