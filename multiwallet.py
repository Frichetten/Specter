# Specter MultiWallet Implementation
# Nick Frichette 12/10/2017

"""The purpose of the multiwallet is to provide an interface for users
    to interact with their Specter wallets. This application will show
    all the wallets thy currently possess, as well as allow users to
    create more."""

import shutil
import copy

from wallet import *
from blockchain import *


def create_wallet(wallet_dict):
    wallet_name = raw_input("What would you like to name the wallet?: ")
    print "Creating " + wallet_name
    return_wallet = copy.copy(wallet_dict)
    return_wallet[wallet_name] = Wallet(wallet_name)
    return return_wallet


def delete_wallet(wallet_dict, wallet_name):
    yn = raw_input("Are you sure you want to delete this wallet? It cannot be undone[y/n]: ")
    if yn == 'n':
        print "Deletion aborted"
    elif yn == 'y':
        name = wallet_name.name
        print "Wallet to delete: " + name
        proof = raw_input("Please type the name of the wallet to finalize decision [" + name + "]: ")
        if proof == name:
            wallet_dict.pop(name, None)
            shutil.rmtree('key-' + name)
        else:
            print "Name improperly typed. Aborting!"


if __name__ == '__main__':

    wallets = {}
    blockchain = Blockchain(is_node=False)

    # The convention for identifying wallets it having the public and
    # private keys in a local directory with the name key-"wallet name"
    for item in os.listdir('.'):
        if 'key-' in item and 'nodekey' not in item:
            wallets[item[item.index('-')+1:]] = Wallet(item)

    # If there are no keys, then we need to offer the chance to make a wallet
    if len(wallets.keys()) == 0:
        ans = raw_input("We didn't find a wallet, would you like to create one? [y/n]: ")
        if ans == 'y':
            wallets = create_wallet(wallets)
        if ans == 'n':
            print "With no keys we'll have to exit. Goodbye"
            exit(0)

    """ Now that we've loaded the wallets, lets give the users some choices """
    ans = ""
    guide = {}
    while ans != 'exit':
        print "\033[H\033[J",  # Note the comma
        print "\rWelcome to Specter Multi_Wallet V0.02"  # \r is to clear that line
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print ""
        print "To begin, select a wallet listed below"
        print ""
        for i, item in enumerate(wallets.keys()):
            guide[i] = item
            print "("+str(i)+") " + wallets[item].name
        print ""
        print "To select a wallet please enter a number and hit [Enter]"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "To create a wallet please enter 'c' and hit [Enter]"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        
        ans = raw_input(">> ")

        # If the input is 'c' we need to create a new wallet
        if ans == 'c':
            wallets = create_wallet(wallets)

        # If the user selects a number, we should check if it is a valid selection
        elif ans != 'exit' and guide[int(ans)] in wallets.keys():
            ians = ""
            twallet = wallets[guide[int(ans)]]
            while ians != 'exit':
                print "\033[H\033[J",  # Note the comma
                print "\r(0) Display Address"  # \r is to clear that line
                print "(1) Send Amount to Other Wallet"
                print "Balance: " + str(twallet.get_balance(twallet.get_address(), blockchain))
                print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                print "To delete this wallet please enter 'd' and hit [Enter]"

                ians = raw_input(twallet.name+">> ")

                # If the input is 'd' we need to delete a wallet
                if ians == 'd':
                    delete_wallet(wallets, twallet)
                    ians = 'exit'
