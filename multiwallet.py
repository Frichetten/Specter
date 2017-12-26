# Specter MultiWallet Implementation
# Nick Frichette 12/10/2017

"""The purpose of the multiwallet is to provide an interface for users
    to interact with their Specter wallets. This application will show
    all the wallets thy currently possess, as well as allow users to
    create more."""

import shutil

from wallet import *
from blockchain import *

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
            name = raw_input("What would you like to name the wallet?: ")
            print "Creating " + name
            wallets[name] = Wallet(name)
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
        print "To delete a wallet please enter 'd' and hit [Enter]"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        
        ans = raw_input(">> ")

        # If the input is 'c' we need to create a new wallet
        if ans == 'c':
            name = raw_input("What would you like to name the wallet?: ")
            print "Creating " + name
            wallets[name] = Wallet(name)

        # If the input is 'd' we need to delete a wallet
        elif ans == 'd':
            name = raw_input("Which wallet would you like to delete?: ")
            ans = raw_input("Are you sure you want to delete this wallet? It cannot be undone[y/n]: ")
            if ans == 'n':
                print "Deletion aborted"
            elif ans == 'y':
                name = wallets[guide[int(name)]].name
                print name
                raw_input("ff")

        # If the user selects a number, we should check if it is a valid selection
        elif ans != 'exit' and guide[int(ans)] in wallets.keys():
            print "\033[H\033[J",  # Note the comma
            ians = ""
            while ians != 'exit':
                print "\r(0) Display Address"  # \r is to clear that line
                print "(1) Send Amount to Other Wallet"
                twallet = wallets[guide[int(ans)]]
                print "Balance: " + str(twallet.get_balance(twallet.get_address(), blockchain))

                ians = raw_input(wallets[guide[int(ans)]].name+">> ")
